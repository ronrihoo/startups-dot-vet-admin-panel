from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, Regexp, EqualTo


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Stay logged in?')


class ScanForm(Form):
    # TODO: convert this into a class to avoid hard-coded repetition (post-prototype).
    vetbiz_title = 'vetbiz'
    vetbiz_url = 'vip.vetbiz.gov/Public/Search/Default.aspx'
    vetbiz_last_scan = 0
    vetbiz_new_data = 0
    vetbiz_data_count = 0
    vetbiz_invoked_by = ''
    vetbiz_scan = SubmitField(label='Scan')
    buyvet_title = 'buyvet'
    buyvet_url = 'buyveteran.com'
    buyvet_last_scan = 0
    buyvet_new_data = 0
    buyvet_data_count = 0
    buyvet_invoked_by = ''
    buyvet_scan = SubmitField(label='Scan')


class CreateUserForm(Form):
    new_user = StringField('Username: ',
                           validators=[DataRequired(),
                                       length(min=3,
                                              max=16,
                                              message="Username Error: length must be between "
                                                      "3 and 16 characters."),
                                       Regexp('^\w+$',
                                              message="Username Error: only alphanumeric "
                                                      "characters are allowed.")
                                       ])
    new_pass = PasswordField('Password: ',
                             validators=[DataRequired(),
                                         EqualTo('confirm_pass',
                                                 message="Password Error: mismatch")
                                         ])
    confirm_pass = PasswordField('Confirm: ',
                                 validators=[DataRequired(),
                                             EqualTo('confirm_pass',
                                                     message="Password Error: mismatch")
                                             ])

    def validate(self):
        # needs to start with alphabetic characters
        if not self.new_user.data.startswith(""):
            return False

        if not self.new_pass.data:
            return False

        if not Form.validate(self):
            return False

        return True
