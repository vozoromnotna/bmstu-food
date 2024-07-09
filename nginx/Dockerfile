FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY bmstufood.crt /etc/nginx/

COPY bmstufood.key /etc/nginx/