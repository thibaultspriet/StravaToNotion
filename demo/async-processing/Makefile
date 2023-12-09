deploy: build deploy_listener deploy_process
	echo "deploying ..."

build:
	zip -FSr deployment_package.zip ./src
	zip deployment_package.zip listener.py
	zip deployment_package.zip process_events.py

deploy_listener:
	aws lambda update-function-code --function-name listener \
	--zip-file fileb://deployment_package.zip --no-cli-pager

deploy_process:
	aws lambda update-function-code --function-name demo_process_events \
	--zip-file fileb://deployment_package.zip --no-cli-pager

tf: build
	$(MAKE) -C terraform-aws-deployment all
