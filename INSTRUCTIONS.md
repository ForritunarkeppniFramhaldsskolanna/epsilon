
sudo ./docker/scripts/data $(pwd)/data:/data $(pwd):/epsilon
sudo ./docker/scripts/database
NAME=fk_2014_beta CONTEST=./example_contests/fk_2014_beta/ DEBUG=true sudo -E docker-compose build
NAME=fk_2014_beta CONTEST=./example_contests/fk_2014_beta/ DEBUG=true sudo -E docker-compose up
NAME=fk_2014_beta CONTEST=./example_contests/fk_2014_beta/ sudo -E docker-compose run --rm epsilon autojudge 1

