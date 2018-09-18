This is pathology - an [Opal](https://github.com/openhealthcare/opal) plugin.

## What problem does it solve?
Pathology is a means to model Pathology tests e.g. Blood Cultures in a simple way with some handy utilities.


## What do the models look like?
In the most basic form a pathology test is just an opal subrecord. It should hold one or more observations.

An observation is the result of a test, this can be numeric or a string. Whatever the result we store it in the `result` field. If the field is numeric we also store it in `result_number` field.

## How do I customise this?
The Pathology model defers most of its methods to a `PathologyCategory`. The Pathology Category is an opal discoverable. You can change `update_from_dict` and `to_dict` methods like you would on a subrecord.
