FROM cloudcix/framework:latest
WORKDIR /application_framework/membership
COPY . .

# Install the requirements
RUN pip3 install -r requirements.txt && pip3 install -r ../app-requirements.txt
RUN cp urls_local.py ../system_conf/urls_local.py && mv settings_local.py ../system_conf/settings_local.py && mv /application_framework/membership/errors /application_framework

WORKDIR /application_framework
ENV CLOUDCIX_ENVIRONMENT live
ENV RELEASE="stable"

# Setup the entrypoint - Migrate the DB changes if there are any, and run gunicorn
EXPOSE 443
ENTRYPOINT python3 manage.py migrate --database=membership membership && gunicorn --bind=0.0.0.0:443 --access-logfile - --log-file - --log-level info --timeout 60 system_conf.wsgi


# To build a membership cron image which allows the cron job to be passed in as the command to send 
# user expiration emails or run integrity tests set entrypoint to the following

# ENTRYPOINT ["python", "manage.py"]
