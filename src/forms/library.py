from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField)


# FORMS
class GameForm(FlaskForm):
    alt_title = StringField(validators=[Length(max=128), Optional()])
    archived = BooleanField()
    co_op = BooleanField()
    collection_id = IntegerField('Collection', validators=[Optional()])
    controller_support = BooleanField()
    date_added = HiddenField()
    date_modified = HiddenField()
    description = TextAreaField(validators=[Length(max=8192), Optional()])
    developer = StringField(validators=[Optional()])
    ESRB_RATINGS = [
        (None, 'None'),
        ('E', 'Everyone'),
        ('E10', 'Everyone 10+'),
        ('T', 'Teen'),
        ('M', 'Mature'),
        ('AO', 'Adults Only')
    ]
    esrb = SelectField('ESRB',
                       choices=ESRB_RATINGS,
                       validators=[Length(max=4), Optional()])
    favorite = BooleanField()
    filename = StringField('File Name',
                           validators=[
                               DataRequired('File Name required.'),
                               Length(max=128)])
    genre_id = IntegerField('Genre', validators=[Optional()])
    gpu = StringField('GPU', validators=[Length(max=64), Optional()])
    hdd = StringField('HDD', validators=[Length(max=64), Optional()])
    mod = StringField('Mod/Engine', validators=[Length(max=64), Optional()])
    notes = TextAreaField(validators=[Length(max=8192), Optional()])
    online_multiplayer = BooleanField()
    operating_system = StringField(validators=[Length(max=64), Optional()])
    platform_id = IntegerField('Platform',
                               validators=[DataRequired('Platform required.')])
    players = IntegerField('Player(s)',
                           validators=[NumberRange(max=64), Optional()])
    processor = StringField('CPU', validators=[Length(max=64), Optional()])
    publisher = StringField(validators=[Length(max=128), Optional()])
    ram = StringField('RAM', validators=[Length(max=64), Optional()])
    REGIONS = [
        (None, 'None'),
        ('NA', 'North America'),
        ('EU', 'Europe'),
        ('JP', 'Japan'),
        ('SK', 'South Korea')
    ]
    region = SelectField(choices=REGIONS,
                         validators=[Length(max=2), Optional()])
    save_path = StringField(validators=[Length(max=256), Optional()])

    steam_id = IntegerField(validators=[NumberRange(max=9999999), Optional()])
    STORE = [
        ('BLIZZARD', 'Blizzard'),
        ('GOG', 'GOG.com'),
        ('HUMBLE', 'Humble Bundle'),
        ('ITCH', 'itch.io'),
        ('PSN', 'PlayStation Network'),
        ('STEAM', 'Steam'),
        ('OTHER', 'Other')
    ]
    store = SelectField(choices=STORE, validators=[Length(max=64), Optional()])
    tags = StringField(validators=[Length(max=256), Optional()])
    title = StringField(validators=[
        DataRequired('Title required.'),
        Length(max=128)])
    translation = BooleanField()
    year = IntegerField(
        validators=[
            NumberRange(
                min=1940,
                max=2999,
                message='Year entered is out of sanity range.'), Optional()])
    submit = SubmitField("Save")


class CollectionForm(FlaskForm):
    name = StringField(validators=[Length(max=128)])
    description = TextAreaField(validators=[Length(max=4096), Optional()])
    submit = SubmitField("Save")


class DeviceForm(FlaskForm):
    name = StringField(validators=[Length(max=128)])
    mnt_path = StringField(validators=[Length(max=128)])
    games_path = StringField(validators=[Length(max=128), Optional()])
    submit = SubmitField("Save")
