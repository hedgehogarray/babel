<?xml version="1.0" encoding="UTF-8" ?>
<Package name="Babel" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="." xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs>
        <Dialog name="Lexicon" src="scripts/butane/dialog/Lexicon/Lexicon.dlg" />
    </Dialogs>
    <Resources>
        <File name="icon" src="icon.png" />
        <File name="main" src="scripts/main.py" />
        <File name="__init__" src="scripts/libs/__init__.py" />
        <File name="qiscript" src="scripts/libs/qiscript.py" />
        <File name="__init__" src="scripts/butane/__init__.py" />
        <File name="conversation" src="scripts/butane/conversation.py" />
        <File name="fuel" src="scripts/butane/fuel.py" />
        <File name="language_utils" src="scripts/butane/language_utils.py" />
        <File name="package_utils" src="scripts/butane/package_utils.py" />
        <File name="LICENSE" src="scripts/libs/mstranslator/LICENSE" />
        <File name="__init__" src="scripts/libs/mstranslator/__init__.py" />
    </Resources>
    <Topics>
        <Topic name="Lexicon_enu" src="scripts/butane/dialog/Lexicon/Lexicon_enu.top" topicName="Lexicon" language="en_US" />
    </Topics>
    <IgnoredPaths>
        <Path src="scripts/butane/tests/TestBehavior/dialog/TestTopic/TestTopic.dlg" />
        <Path src="scripts/butane/tests/test_package_utils.py" />
        <Path src="scripts/butane/tests/test_butane.py" />
        <Path src="scripts/butane/tests/README" />
        <Path src="scripts/butane/tests/lu_string_test.json" />
        <Path src="scripts/butane/tests/TestBehavior/dialog/TestTopic" />
        <Path src="scripts/butane/README" />
        <Path src="scripts/butane/tests/TestBehavior" />
        <Path src="scripts/butane/tests/test_language_utils.py" />
        <Path src="scripts/butane/tests/TestBehavior/Test.pml" />
        <Path src="scripts/butane/.git" />
        <Path src="scripts/butane/tests/TestBehavior/behavior.xar" />
        <Path src="scripts/butane/tests/__init__.py" />
        <Path src="scripts/libs/qiscript.pyc" />
        <Path src="scripts/butane/tests/test_conversation.py" />
        <Path src="scripts/butane/tests/TestBehavior/manifest.xml" />
        <Path src="scripts/butane/tests/conftest.py" />
        <Path src="scripts/butane/tests/TestBehavior/dialog/TestTopic/TestTopic_enu.top" />
        <Path src="scripts/butane/tests/TestBehavior/.metadata" />
        <Path src="scripts/libs/__init__.pyc" />
        <Path src="scripts/butane/tests/TestBehavior/dialog" />
        <Path src="scripts/butane/.gitignore" />
        <Path src="scripts/butane/tests/test_fuel.py" />
    </IgnoredPaths>
</Package>
