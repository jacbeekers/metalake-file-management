source venv/bin/activate
pip3 install pdoc3 pydeps >/dev/null
##
##
PACKAGE_NAME=adls_management
#
pdoc3 --force --output-dir docs/$PACKAGE_NAME/markdown src/$PACKAGE_NAME
pdoc3 --force --html --output-dir docs/$PACKAGE_NAME/html src/$PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o docs/$PACKAGE_NAME/${PACKAGE_NAME}.svg src/$PACKAGE_NAME

##
##
PACKAGE_NAME=interface_file_management
#
pdoc3 --force --output-dir docs/$PACKAGE_NAME/markdown src/$PACKAGE_NAME
pdoc3 --force --html --output-dir docs/$PACKAGE_NAME/html src/$PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o docs/$PACKAGE_NAME/${PACKAGE_NAME}.svg src/$PACKAGE_NAME
##
##
PACKAGE_NAME=utils
#
pdoc3 --force --output-dir docs/$PACKAGE_NAME/markdown src/$PACKAGE_NAME
pdoc3 --force --html --output-dir docs/$PACKAGE_NAME/html src/$PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o docs/$PACKAGE_NAME/${PACKAGE_NAME}.svg src/$PACKAGE_NAME
##
# generate dependency graph for everything in metalake_management
pydeps --log ERROR -o docs/overall.svg src

