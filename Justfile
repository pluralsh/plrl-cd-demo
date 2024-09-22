release vsn:
	git checkout main; \
	git pull --rebase; \
	git tag -a {{vsn}} -m "new release"; \
	git push origin {{vsn}}