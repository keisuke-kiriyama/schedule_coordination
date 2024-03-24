FROM python:3.9.15
RUN pip install --upgrade pip
RUN pip install gspread
RUN pip install oauth2client
RUN pip install google-api-python-client
RUN pip install google-auth
RUN pip install google-auth-httplib2
RUN pip install google-auth-oauthlib
