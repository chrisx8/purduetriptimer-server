import secrets
import string
from datetime import datetime
from flask import Flask, request, make_response
from os import environ

from models import DBSession, Trip


# generate random session key
def create_session_key(length):
    key = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        key += secrets.choice(characters)
    return key

# create the webapp and api instances
app = Flask(__name__, instance_relative_config=True)

# create app configurations
app.config.from_mapping(
    SECRET_KEY=create_session_key(64),        # make a secret key (length 64)
    DATABASE_URL=environ.get('DATABASE_URL')  # database URL. supports sqlite, mysql, postgresql
)


# validate building is a Purdue building
def validate_building(building):
    PURDUE_BUILDINGS = {"ADPA-C - Aspire at Discovery Park",
        "AERO - Aerospace Science Laboratory", "AQUA - Boilermaker Aquatic Center",
        "ARMS - Armstrong Hall of Engineering", "BCHM - Biochemistry Building", "BIND - Bindley Bioscience Center",
        "BRNG - Beering Hall of Liberal Arts and Education", "BRWN - Brown Laboratory of Chemistry",
        "CARY - Cary Quadrangle", "CL50 - Class of 1950 Lecture Hall", "CREC - Co-Rec",
        "CRTN - Hobart and Russell Creighton Hall of Animal Sciences", "EE - Electrical Engineering Building",
        "EHSB - Equine Health Sciences Building", "ELLT - Elliott Hall of Music", "ERHT - Earhart Residence Hall",
        "FORD - Ford Dining Court", "FRNY - Forney Hall of Chemical Engineering", "FST - First Street Towers",
        "GRFN - Griffin Residence Hall North", "GRFS - Griffin Residence Hall South (Third Street Suites)",
        "HAAS - Haas Hall", "HAMP - Hampton Hall of Civil Engineering",
        "HANS - Hansen Life Sciences Research Building", "HARR - Harrison Residence Hall",
        "HAWK - Hawkins Hall", "HCRN - Honors College and Residences North",
        "HCRS - Honors College and Residences South", "HIKS - Hicks Undergraduate Library",
        "HILL - Hillenbrand Residence Hall", "HLAB - Herrick Laboratories", "HLTP - Hilltop Apartments",
        "HOVD  - Hovde Hall of Administration", "JNSN - Johnson Hall of Nursing", "KNOY - Knoy Hall of Technology",
        "KRCH - Krach Leadership Center", "LILY - Lilly Hall of Life Sciences",
        "LWSN - Lawson Computer Science Building", "LYNN - Lynn Hall of Veterinary Medicine", "MACK - Mackey Arena",
        "MATH - Mathematical Sciences Building", "MCUT - McCutcheon Residence Hall",
        "ME - Mechanical Engineering Building", "MJIS - Jischke Hall of Biomedical Engineering",
        "MRDH - Meredith Residence Hall", "MRDS - Meredith Residence Hall South", "MRRT - Marriott Hall",
        "MTHW - Matthews Hall", "OWEN - Owen Residence Hall", "PHYS - Physics Building",
        "PMU - Purdue Memorial Union", "PUSH - Purdue University Student Health Center", "PVIL - Purdue Village",
        "REC - Recitation Building", "RHPH - Heine Pharmacy Building", "SCHL - Schleman Hall of Student Services",
        "SHRV - Shreve Residence Hall", "SMLY - Smalley Center for Housing and Food Services Administration",
        "SMTH - Smith Hall", "STDM - Ross-Ade Stadium", "STEW - Stewart Center", "STON - Stone Hall",
        "TARK - Tarkington Residence Hall", "TREC - Turf Recreation Exercise Center", "UNIV - University Hall",
        "WALC - Wilmeth Active Learning Center", "WDCT - Wiley Dining Court", "WILY - Wiley Residence Hall",
        "WNSR - Windsor Residence Halls", "YONG - Young Hall"
    }
    return building in PURDUE_BUILDINGS


# validate travel method is supported
def validate_method(method):
    TRAVEL_METHODS = {"Biking", "Driving", "E-Scooter", "Skateboarding", "Walking"}
    return method in TRAVEL_METHODS


@app.route('/')
def homepage():
    return ''


@app.route('/trips/', methods=('GET', 'POST'))
def serve_trips():
    def build_get_response(data):
        text = ''
        for i in data:
            text += f'{i.from_building},{i.to_building},{i.method},{i.time}\n'

        resp = make_response(text, 200)
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    # store trip to DB. return (message, status code, header)
    def store_trip(from_bldg, to_bldg, method, time, timestamp):
        # convert time to int
        time = int(time)
        # validate all input
        if (not validate_building(from_bldg) or not validate_building(to_bldg) or not validate_method(method)):
            return ("Your input is invalid! Please try again.", 400)
            code = 400
        elif (time < 1):
            return ("Your time seems really short... Have you started the timer?", 400)

        trip = Trip(from_building=from_bldg, to_building=to_bldg, method=method, time=time, timestamp=timestamp)
        DBSession.add(trip)
        DBSession.commit()
        DBSession.close()

        return ("Thank you! Your trip has been recorded.", 201)

    # GET: all trip entries
    if request.method == 'GET':
        all_trips = DBSession.query(Trip).all()
        DBSession.close()
        
        return build_get_response(all_trips)

    # POST: add user-reported trip to DB
    if request.method == 'POST':
        # get all fields
        data = request.data
        current_time = datetime.now()

        # rate limit: check if there's an exact match within 30sec
        # find trip with identical attributes
        identical_trips = DBSession.query(Trip).filter_by(from_building=data['from'], to_building=data['to'], 
                           method=data['method'], time=data['time']).order_by(Trip.id.asc())
        if identical_trips.count() > 0:
            # find most recent trip with identical identifiers
            trip = identical_trips[-1]

            # calculate time diff
            time_diff = current_time - trip.timestamp
            time_diff_second = time_diff.total_seconds()
            # less than 30sec time delta: http 429
            if (time_diff_second < 30):
                (message,code) = ("429 Too Many Requests", 429)
            else:
                (message, code) = store_trip(data['from'], data['to'], data['method'], data['time'], current_time)
        else:
            (message, code) = store_trip(data['from'], data['to'], data['method'], data['time'], current_time)

        # build and send response
        response = make_response(message, code)
        response.header['Content-Type'] = 'text/plain'
        return response
    