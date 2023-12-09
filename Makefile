deploy: build deploy_webhook deploy_process
	echo "deploying ..."

build: reset_build build_src build_dep

reset_build:
	rm -f deployment_package.zip
	rm -r -f dependencies

build_src:
	zip -FSr -x@exclude.lst deployment_package.zip ./src
	zip deployment_package.zip lambda_function.py
	zip deployment_package.zip lambda_process_events.py

build_dep:
	poetry export -f requirements.txt --without-hashes --without-urls -o requirements.txt
	pip install --target ./dependencies -r requirements.txt
	cd dependencies; zip -r ../deployment_package.zip .

deploy_webhook:
	aws lambda update-function-code --function-name strava_webhook \
	--zip-file fileb://deployment_package.zip --no-cli-pager

deploy_process:
	aws lambda update-function-code --function-name process_events \
	--zip-file fileb://deployment_package.zip --no-cli-pager

tf:
	$(MAKE) -C terraform-aws-deployment all
