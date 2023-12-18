FROM filebrowser/filebrowser

ARG PUID
ARG PGID

RUN mkdir /app &&\
    chown --quiet -R $PUID:$PGID /app

USER $PUID:$PGID
ENV FB_DATABASE=/app/database.db
RUN /filebrowser config init \
      --auth.method=noauth &&\
    /filebrowser users add admin admin \
      --perm.admin=false \
      --perm.create=true \
      --perm.delete=false \
      --perm.download=true \
      --perm.execute=false \
      --perm.modify=true \
      --perm.rename=false \
      --perm.share=false
