# tup-edu-erp

Education ERP for TUP

## Setting

### Make custom-addons folder

Make folder named 'custom-addons' under odoo11

```bash
\odoo11\> mkdir custom-addons
\odoo11\> cd custom-addons
\odoo11\custom-addons\> _
```

### Clone git repository

```bash
\odoo11\custom-addons\> git clone https://github.com/oberak/tup_edu_erp.git
```

### Set a Git username

```bash
\> git config --global user.name "Your github.com user name"
```

## Install Educational ERP modules

Copy Educational ERP modules to 'custom-addons'
\odoo11\custom-addons\education_core
\odoo11\custom-addons\education_theme
\odoo11\custom-addons\education_attendances
\odoo11\custom-addons\education_exam
\odoo11\custom-addons\education_fee
\odoo11\custom-addons\education_promotion
\odoo11\custom-addons\education_time_table
\odoo11\custom-addons\educational_announcement

### Modify odoo11/odoo.conf

Use your real path
addons_path = E:\dev\odoo11\addons,E:\dev\odoo11\custom-addons

## Run odoo11

```bash
\dev> env-odoo11\Scripts\activate.bat
(env-odoo11) E:\dev> cd odoo11
(env-odoo11) E:\dev\odoo11\> python odoo-bin
```

## Install modules to odoo

- Visit: localhost:8069

- Go to 'Settins' Page

  - Click 'Activate the developer mode' on right-bottom side

  - Click 'Update Apps List' on left-menu

  - Delete 'Apps' filter on search box

  - Search 'Education' and install all modules
