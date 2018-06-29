IMAGE=$(shell basename $(shell pwd))
REGISTRY=registry.hub.docker.com
APP_NAME=$(IMAGE)
#账号名称
REGISTRY_USER=siskinc

FQIN=$(REGISTRY_USER)/$(IMAGE)

build:
	# echo "docker build -t $(FQIN) --build-arg PROJECT_NAME=$(APP_NAME) ."
	# docker rmi $(APP_NAME)
	# docker build -t $(FQIN) --build-arg PROJECT_NAME=$(APP_NAME) .
	docker-compose build 

up:
	docker-compose up -d --force-recreate
	
down:
	docker-compose down

spider_build:
	docker build -t $(FQIN) --build-arg PROJECT_NAME=$(APP_NAME) .

spider_rm:
	docker rmi $(FQIN)