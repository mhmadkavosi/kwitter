FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./req.txt /var/www/req.txt
RUN pip install -r /var/www/req.txt
COPY ./app /app
