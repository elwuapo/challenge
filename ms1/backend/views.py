# Importaciones de python
import random
from datetime import datetime, timedelta

# Importaciones de django
from django.shortcuts import render
from django.core import serializers

# Importaciones de librerias
from rest_framework.views import APIView
from rest_framework.response import Response
from faker import Faker

# Importaciones de modulos
from backend.models import Punch as PunchModel
from backend.models import Report as ReportModel
from backend.models import Person as PersonModel

faker = Faker()

# Endpoint para realizar insertsiones random en la tabla de Punch
class Punch(APIView):    
    # Endpoint que crea marcas de entrada y salida de forma random los ultimos 7 dias para cada empleado:
    def post(cls, request):
        try:
            now      = datetime.now()
            dates    = list()
            response = list()

            for i in range(7):
                date = now - timedelta(days=i)

                hour   = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)

                datetime_1 = date.replace(hour=hour, minute=minute, second=second)

                hour   = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)

                datetime_2 = date.replace(hour=hour, minute=minute, second=second)
                
                start = datetime_1 if datetime_1 < datetime_2 else datetime_2
                end   = datetime_2 if datetime_2 > datetime_1 else datetime_1

                dates.append((start, end))

            # Imprimir la lista de fechas
            for person in PersonModel.objects.all():
                for start, end in dates:
                    punch_in = PunchModel.objects.create(
                        type = 'in',
                        punch_time = start,
                        person_id = person.pk
                    )

                    punch_out = PunchModel.objects.create(
                        type = 'out',
                        punch_time = end,
                        person_id = person.pk
                    )

                    response.append({
                        'punch_id': punch_in.pk,
                        'type': punch_in.type,
                        'punch_time': punch_in.punch_time,
                        'person_id': punch_in.person_id
                    })

                    response.append({
                        'punch_id': punch_out.pk,
                        'type': punch_out.type,
                        'punch_time': punch_out.punch_time,
                        'person_id': punch_out.person_id
                    })

            return Response(response, status=201)
        
        except Exception as e:
            print(e)
            return Response(status=400)
    
    # Elimina todos los elementos de la tabla Punch
    def delete(cls, request):
        try:
            PunchModel.objects.all().delete()
            return Response(status=204)
        except Exception as e:
            print(e)
            return Response(status=400) 
    
class Person(APIView):
    def get(cls, request):
        try:
            persons = PersonModel.objects.all()
            response = list()

            for person in persons:
                response.append({
                    'person_id': person.person_id,
                    'name': person.name,
                    'email': person.email
                })

            return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(status=400)
    
    def post(cls, request):
        try:
            # Endpoint que crea empleados de forma random:
            # body = { count: 10 }
            amount = int(request.data.get('amount'))
            response = list()

            if(amount):    
                for i in range(amount):
                    person = PersonModel.objects.create(
                        name='{firstname} {lastname}'.format(firstname=faker.first_name(), lastname=faker.last_name()),
                        email=faker.email()
                    )

                    response.append({
                        'person_id': person.person_id,
                        'name': person.name,
                        'email': person.email
                    })

                return Response({'persons': response}, status=201)
            else:
                return Response(status=400)
            
        except Exception as e:
            print(e)
            return Response(status=400)
    
    def delete(cls, request):
        # Elimina todos los elementos de la tabla Person
        try:
            PersonModel.objects.all().delete()
            return Response(status=204)
        except:
            return Response(status=400)
    
class Report(APIView):
    # Endpoint para obtener un reporte por su id o el listado de todos los reportes
    def get(cls, request):
        try:
            if request.query_params.get('id'):
                id     = int(request.query_params.get('id'))
                report = ReportModel.objects.get(report_id = id)
                
                response = {
                    'report_id': report.report_id,
                    'status': report.status,
                    'filename': report.filename,
                    'path': report.path,
                    'url': report.url
                }

                return Response(response, status=200)
            else:
                reports = ReportModel.objects.all()

                response = list()

                for report in reports:
                    response.append({
                        'report_id': report.report_id,
                        'status': report.status,
                        'filename': report.filename,
                        'path': report.path,
                        'url': report.url
                    }) 

                return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(status=400)
    
    # Endpoint que crea un reporte en la tabla Report 
    # body = { person_id: <id> }
    def post(cls, request):
        try:
            person_id = int(request.data.get('person_id'))

            if person_id:
                person  = PersonModel.objects.get(person_id = person_id)
                punches = PunchModel.objects.filter(person_id = person_id)

                filename = 'report_{str_datetime}.txt'.format(str_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
                path     = './static/reports/{filename}'.format(filename = filename)
                url      = 'http://localhost:8000/static/reports/{filename}'.format(filename = filename)

                report = ReportModel.objects.create(
                    status='pending',
                    filename=filename, 
                    path=path,
                    url=url
                )

                report.status = 'creating'
                report.save()

                lines = [
                    'Reporte de asistencia de {name}'.format(name=person.name),
                    'Fecha de creacion: {datetime}'.format(datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    'Marcas de entrada y salida: ',
                    'Nota: las fechas estan en formato UTC-0 para su facil conversion',
                    '----------------------------------------------------------------',
                ]

                for punch in punches:
                    if(punch.type == 'in'):
                        lines.append('{type} : {datetime}'.format(type=punch.type, datetime=punch.punch_time.strftime("%Y-%m-%d %H:%M:%S")))
                    else:
                        lines.append('{type}: {datetime}'.format(type=punch.type, datetime=punch.punch_time.strftime("%Y-%m-%d %H:%M:%S")))

                with open(path, 'w') as f:
                    f.write('\n'.join(lines))

                report.status = 'created'
                report.save()
                
                response = {
                    'report_id': report.report_id,
                    'status': report.status,
                    'filename': report.filename,
                    'path': report.path,
                    'url': report.url
                }
                                                
                return Response(response, status=201)
            else:
                return Response(status=400)
            
        except Exception as e:
            print(e)
            return Response(status=400)

class Check(APIView):
    def get(cls, request):
        try:
            id       = int(request.query_params.get('id'))
            report   = ReportModel.objects.get(report_id = id)
            response = {
                'status': report.status,
            }

            return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(status=400)