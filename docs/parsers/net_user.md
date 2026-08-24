[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.net_user"></a>

# jc.parsers.net_user

jc - JSON Convert `net user` command output parser


Usage (cli):

    $ net users | jc --net-user
    $ net users /domain | jc --net-user
    $ net users User1 | jc --net-user
    $ net users User1 /domain | jc --net-user

Usage (module):

    import jc
    result = jc.parse('net_user', net_user_command_output)

Schema:

    {
        "domain":                             string,
        "account_origin":                     string,
        "user_accounts": [
            {
                "user_name":                  string,
                "full_name":                  string,
                "comment":                    string,
                "user_comment":               string,
                "country_region_code":        string,
                "account_active":             boolean,
                "account_expires":            string,
                "password_last_set":          string,
                "password_expires":           string,
                "password_changeable":        string,
                "password_required":          boolean,
                "user_may_change_password":   boolean,
                "workstations_allowed":       string,
                "logon_script":               string,
                "user_profile":               string,
                "home_directory":             string,
                "last_logon":                 string,
                "logon_hours_allowed":        string,
                "local_group_memberships": [
                                              string,
                ],
                "global_group_memberships": [
                                              string,
                ]
            }
        ]
    }


Examples:

    $ net users | jc --net-user -p
    {
        "account_origin": "\\\\WIN-SERVER16",
        "domain": "",
        "user_accounts": [
            {
                "user_name": "Administrator"
            },
            {
                "user_name": "DefaultAccount"
            },
            {
                "user_name": "Guest"
            },
            {
                "user_name": "pentera_BnlLQVnd7p"
            },
            {
                "user_name": "user1"
            }
        ]
    }

    $ net users /domain | jc --net-user -p
    {
        "account_origin": "\\\\DESKTOP-WIN10-PRO.somecompany.corp",
        "domain": "somecompany.corp",
        "user_accounts": [
            {
                "user_name": "aaron"
            },
            {
                "user_name": "addison"
            },
            {
                "user_name": "Administrator"
            },
            {
                "user_name": "ansible"
            },
            {
                "user_name": "da"
            },
            {
                "user_name": "DefaultAccount"
            },
            {
                "user_name": "Guest"
            },
            {
                "user_name": "harrison"
            },
            {
                "user_name": "james"
            },
            {
                "user_name": "krbtgt"
            },
            {
                "user_name": "liam"
            },
            {
                "user_name": "localadmin"
            },
            {
                "user_name": "tiffany"
            }
        ]
    }

    $ net users Administrator | jc --net-user -p
    {
        "domain": "",
        "user_accounts": [
            {
                "account_active": true,
                "account_expires": "Never",
                "comment": "Built-in account for administering the computer/domain",
                "country_region_code": "000 (System Default)",
                "global_group_memberships": [],
                "last_logon": "2024-08-23T13:47:11",
                "local_group_memberships": [
                    "Administrators"
                ],
                "logon_hours_allowed": "All",
                "password_changeable": "2021-12-17T11:07:14",
                "password_expires": "2022-01-27T11:07:14",
                "password_last_set": "2021-12-16T11:07:14",
                "password_required": true,
                "user_may_change_password": true,
                "user_name": "Administrators",
                "workstations_allowed": "All"
            }
        ]
    }

    $ net users Administrator /domain | jc --net-user -p | jq
    {
        "domain": "somecompany.corp",
        "user_accounts": [
            {
                "account_active": true,
                "account_expires": "Never",
                "comment": "Built-in account for administering the computer/domain",
                "country_region_code": "000 (System Default)",
                "global_group_memberships": [
                    "Domain Admins",
                    "Domain Users",
                    "Group Policy Creator",
                    "Enterprise Admins",
                    "Schema Admins"
                ],
                "last_logon": "2024-07-17T13:46:12",
                "local_group_memberships": [
                    "Administrators"
                ],
                "logon_hours_allowed": "All",
                "password_changeable": "2023-09-30T11:44:26",
                "password_expires": "Never",
                "password_last_set": "2023-09-29T11:44:26",
                "password_required": true,
                "user_may_change_password": true,
                "user_name": "Administrators",
                "workstations_allowed": "All"
            }
        ]
    }

<a id="jc.parsers.net_user.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Parsed dictionary. The raw and processed data structures are the same.

### Parser Information
Compatibility:  win32

Source: [`jc/parsers/net_user.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/net_user.py)

Version 1.0 by joehacksalot (joehacksalot@gmail.com)
