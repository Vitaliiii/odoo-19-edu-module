# Спочатку абстрактна модель!
from . import person

# Потім моделі, що її використовують, та інші базові моделі
from . import doctor
from . import patient
from . import contact_person
from . import disease
from . import visit

# Потім моделі, які посилаються на попередні (хоча Odoo вміє це розрулювати, але краще так)
from . import diagnosis
from . import specialty
from . import doctor_schedule
from . import doctor_history