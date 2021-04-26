# streamupload
Proof-of-concept app for storing binary experiment data, such as (streaming) video. Its current primary intended use case is with [jspsych-cam-rec](https://github.com/UiL-OTS-labs/jspsych-cam-rec).

## Administration
Basic administrative functions are currently provided by the default Django admin interface. It can be found at https://<base_url>/admin/. Staff users can use the admin interface to add or remove users, groups, tokens, and uploads. Non-staff users can view and download uploaded files.

## To-do

- Connect to university LDAP
- Easier differentiation of participants
- Management of uploads by non-staff users
