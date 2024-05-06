from flask import Blueprint, jsonify, request
from app.services import BookingService
from app.mapping.booking_schema import BookingSchema
from app.dto import ResponseBuilder
from app.validators import validate_with, validate_exists

ps = BookingSchema(many=True) # Para devolver varios departamentos

booking = Blueprint('booking', __name__)

booking_schema = BookingSchema() # Para devolver una reserva
booking_service = BookingService()
response = ResponseBuilder()


@booking.route('/', methods=['GET'])
def index():
    response.add_status_code(200).add_message('Welcome to booking service!').add_data()
    return jsonify(response.build()), response.status_code

@booking.route('/create', methods=['POST'])
@validate_with(BookingSchema)
def create(validated_data):
    booking = validated_data
    user_id = request.args.get('user_id')
    apartment_id = request.args.get('apartment_id')
    response.add_status_code(201).add_message('Booking created!').add_data(
        {"booking": booking_schema.dump(booking_service.create(booking, user_id, apartment_id))}
    )
    return jsonify(response.build()), response.status_code
    
    
@booking.route('/findall', methods=['GET'])
def find_all():
    if not booking_service.find_all():
        response.add_status_code(400).add_message('There are no bookings created!').add_data()
        return jsonify(response.build()), response.status_code
    response.add_status_code(200).add_message('Bookings found!').add_data({"bookings": ps.dump(booking_service.find_all())})
    return jsonify(response.build()), response.status_code
    
    
@booking.route('/findbyid/<int:id>', methods=['GET'])
@validate_exists(booking_service, response)
def find_by_id(id):
    response.add_status_code(200).add_message('Booking found!').add_data({"booking": booking_schema.dump(booking_service.find_by_id(id))})
    return jsonify(response.build()), response.status_code
    
    
@booking.route('/update/<int:id>', methods=['PUT'])
@validate_with(BookingSchema)
@validate_exists(booking_service, response)
def update(validated_data, id):
    booking = validated_data
    response.add_status_code(200).add_message('Booking updated!').add_data(
        {"booking updated": booking_schema.dump(booking_service.update(booking, id))}
    )
    return jsonify(response.build()), response.status_code