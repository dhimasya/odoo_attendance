{
    'name': 'Attendance Machine Integration',
    'version': '12.0.1.0.0',
    'summary': 'Integrate attendance machine with attendance',
    'category': 'Human Resources',
    'author': 'PortCities Ltd',
    'website': 'https://portcities.net',
    'contributors': [
        'Dhimas Yudangga A',
    ],
    'depends': [
        'base', 'hr_attendance',
    ],
    'external_dependencies': {
        'python': [
            'zk',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_machine_views.xml',
        'views/hr_machine_report_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
