from odoo import models, api, fields
from odoo.exceptions import ValidationError


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    cus_name = fields.Char(string='أسم العميل', )  # Customer Name
    cus_phone = fields.Char(string='رقم الهاتف', )  # Phone Number
    alt_phone = fields.Char(string='رقم أخر')  # Alternate Phone
    cus_region = fields.Char(string='منطقة السكن', )  # Region
    cus_source = fields.Selection([
        ('social_media', 'وسائل التواصل الاجتماعي'),
        ('referral', 'إحالة'),
        ('other', 'أخرى'),
    ], string='عرفتنا منين')  # How did you hear about us
    project_name = fields.Char(string='اسم المشروع')
    communication_method = fields.Selection(
        selection=[
            ('whatsapp', 'WhatsApp'),
            ('call', 'Call'),
            ('visit', 'زياره')
        ],
        string="طريقة التواصل",
        required=False , default='whatsapp' # Make it required based on logic in XML view
    )
    # Project Name
    communication_method_stage = fields.Selection([
        ('phone', 'هاتف'),
        ('email', 'بريد إلكتروني'),
        ('whatsapp', 'واتساب'),
        ('other', 'أخرى'),
    ], string='طريقة التواصل')
    is_lead = fields.Boolean(string="", compute='compute_is_lead')
    brand = fields.Char(string="الماركة", required=False)
    model = fields.Char(string="الموديل", required=False)
    manufacture_year = fields.Char(string="سنة الصنع", required=False)
    color = fields.Char(string="اللون", required=False)
    paint_condition = fields.Char(string="حالة الدهان", required=False)
    additional_notes = fields.Text(string="ملاحظات أضافية", required=False)
    odometer = fields.Integer(string="عداد كام", required=False)
    vehicle_category = fields.Char(string="فئة السياره", required=False)
    transmission = fields.Char(string="ناقل الحركة", required=False)
    category = fields.Char(string="الفئة", required=False, default="جميع الفئات")
    initial_price = fields.Float(string="السعر المبدئي", required=False)

    @api.depends('partner_id')
    def compute_is_lead(self):
        for rec in self:
            rec.is_lead = True if rec.type == 'lead' else rec.is_lead == False
            print('is_lead', rec.is_lead)

    car_ownership_date = fields.Date(string='تاريخ أمتلاك السياره')
    engine_type_1 = fields.Char(string='نوع الموتور 1')
    engine_type_2 = fields.Char(string='نوع الموتور 2')
    accessories = fields.Many2many(
        'product.attribute.value',
        'lead_accessory_rel', 'lead_id', 'accessory_id',
        string='الكماليات'
    )
    spare_key = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='المفتاح الاحتياطي')
    average_market_price = fields.Float(string='متوسط سعر السوق')

    # License Details
    name_on_license = fields.Char(string='الأسم المدون علي الرخصه')
    license_plate_number = fields.Char(string='رقم اللوحات')
    chassis_number = fields.Char(string='رقم الشاسية')
    traffic_unit = fields.Char(string='وحده المرور')
    engine_number = fields.Char(string='رقم الموتور')
    date_of_issue = fields.Date(string='تاريخ التحرير')
    inspection_date = fields.Date(string='تاريخ الفحص')
    expiration_date = fields.Date(string='تاريخ الأنتهاء')
    number_of_powers_of_attorney = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('none', 'لايوجد')], string='عدد التوكيلات')
    sale_ban = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='حظر بيع')
    risk_party = fields.Char(string='جهة الخطر')
    monthly_installment_value = fields.Float(string='قيمه القسط الشهري')
    cash_payment_amount = fields.Float(string='مبلغ السداد كاش')

    # Maintenance Information
    maintenance_location = fields.Selection(
        [('agency', 'توكيل'), ('authorized_center', 'مركز خدمة معتمدة'), ('external_workshop', 'ورش خارجية')],
        string='مكان الصيانة')
    chosen_location = fields.Char(string='مكان الأختيار')
    maintenance_notes = fields.Text(string='ملاحظات')

    # Car Add-ons (Attachment fields)
    license_front_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_license_front_rel',  # Relation table name
        'lead_id',  # Column for this model
        'attachment_id',  # Column for the related model
        string='صورة وجهه الرخصه',
        help='Attach the front image of the license.'
    )
    license_back_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_license_back_rel',
        'lead_id',
        'attachment_id',
        string='صورة ظهر الرخصه',
        help='Attach the back image of the license.'
    )
    owner_id_card_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_owner_id_card_rel',
        'lead_id',
        'attachment_id',
        string='صورة بطاقة المالك',
        help='Attach the owner\'s ID card.'
    )
    power_of_attorney_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_power_of_attorney_rel',
        'lead_id',
        'attachment_id',
        string='صورة التوكيل',
        help='Attach the power of attorney.'
    )
    maintenance_invoices_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_maintenance_invoices_rel',
        'lead_id',
        'attachment_id',
        string='صورة فواتير الصيانة',
        help='Attach maintenance invoices.'
    )
    license_inquiry_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_license_inquiry_rel',
        'lead_id',
        'attachment_id',
        string='صورة استعلام الرخصه',
        help='Attach license inquiry documents.'
    )
    power_of_attorney_receipt_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_power_of_attorney_receipt_rel',
        'lead_id',
        'attachment_id',
        string='صورة أستلام التوكيل',
        help='Attach the attorney receipt.'
    )
    additional_image = fields.Many2many(
        'ir.attachment',
        'crm_lead_additional_image_rel',
        'lead_id',
        'attachment_id',
        string='أي صوره إضافية',
        help='Attach any additional images.'
    )

    # Pricing and Commission
    final_price = fields.Float(string='السعر النهائي')
    selling_commission = fields.Float(string='عمولة البيع')
    button_invisible = fields.Boolean(string="button Invisible", compute='compute_button_invisible')
    previous_stage = fields.Boolean(string="button Invisible", compute='compute_previous_stage')
    first_stage_id = fields.Many2one('crm.stage', string="First Stage", compute='_compute_first_stage', store=True)
    is_first_stage = fields.Boolean(string="Is First Stage", compute='_compute_is_first_stage')
    stage_seq = fields.Integer(compute='compute_stage_seq')
    right_front_fender = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Right Front Fender"
    )
    right_front_door = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Right Front Door"
    )
    right_rear_door = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Right Rear Door"
    )
    right_rear_fender = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Right Rear Fender"
    )
    hood = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Hood"
    )
    roof = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Roof"
    )
    tail_gate = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Tail Gate"
    )
    front_bumper = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Front Bumper"
    )
    left_front_fender = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Left Front Fender"
    )
    left_front_door = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Left Front Door"
    )
    left_rear_door = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Left Rear Door"
    )
    left_rear_fender = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Left Rear Fender"
    )
    rear_bumper = fields.Selection(
        [('factory', 'مصنع'), ('paint', 'دهان')],
        string="Rear Bumper"
    )

    # Exterior accessories
    right_front_headlight = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Front Headlight"
    )
    left_front_headlight = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Front Headlight"
    )
    right_front_fog = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Front Fog"
    )
    left_front_fog = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Front Fog"
    )
    front_grill = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Front Grill"
    )
    right_front_mirror = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Front Mirror"
    )
    left_front_mirror = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Front Mirror"
    )
    right_rear_headlight = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Rear Headlight"
    )
    left_rear_headlight = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Rear Headlight"
    )
    windshield = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Windshield"
    )
    rear_glass = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Rear Glass"
    )
    right_front_door_glass = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Front Door Glass"
    )
    right_rear_door_glass = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Right Rear Door Glass"
    )
    left_front_door_glass = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Front Door Glass"
    )
    left_rear_door_glass = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Left Rear Door Glass"
    )
    plate_back_light = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Plate Back Light"
    )
    door_strips = fields.Selection(
        [('original', 'أصلي'), ('non_original', 'غير أصلي')],
        string="Door Strips"
    )

    # Interior parts
    front_shutter = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="ستارة امامية"
    )
    front_left_chassis = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شاسية امامي شمال"
    )
    front_right_chassis = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شاسية امامي يمين"
    )
    right_cartira = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="كارتيره يمين"
    )
    left_cartira = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="كارتيرة شمال"
    )
    front_right_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم امامي يمين"
    )
    middle_right_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم وسط يمين"
    )
    rear_right_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم خلفي يمين"
    )
    rear_fender_right = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="داير رفرف خلفي يمين"
    )
    right_trunk_sword = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شنطه يمين"
    )
    trunk_shutter = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="ستارة شنطة"
    )
    spare_wheel_case = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="حلة الاستبن"
    )
    rear_left_chassis = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شاسية خلفي شمال"
    )
    rear_right_chassis = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شاسيه خلفي يمين"
    )
    left_trunk_sword = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="سلاح شنطة شمال"
    )
    rear_fender_left = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="داير رفرف خلفي شمال"
    )
    rear_left_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم خلفي شمال"
    )
    middle_left_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم وسط شمال"
    )
    front_left_frame = fields.Selection(
        [('factory', 'مصنع'), ('painted', 'بها دهان')],
        string="قايم امامي شمال"
    )
    # Available Parts
    sun_roof = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Sun Roof Availability"
    )
    sun_roof_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Sun Roof Status",
        help="Appears only if Sun Roof is available."
    )

    internal_lights = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Internal Lights Availability"
    )
    internal_lights_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Internal Lights Status",
        help="Appears only if Internal Lights are available."
    )
    black_out_mirror = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Black Out Mirror Availability"
    )
    black_out_mirror_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Black Out Mirror Status"
    )

    dashboard = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Dashboard Availability"
    )
    dashboard_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Dashboard Status"
    )

    multi_function = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Multi-function Availability"
    )
    multi_function_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Multi-function Status"
    )

    electric_mirrors = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Electric Mirrors Availability"
    )
    electric_mirrors_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Electric Mirrors Status"
    )

    electric_windows = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Electric Windows Availability"
    )
    electric_windows_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Electric Windows Status"
    )

    abs_ebd = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="ABS EBD Availability"
    )
    abs_ebd_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="ABS EBD Status"
    )

    windshield_wiper = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Windshield Wiper Availability"
    )
    windshield_wiper_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Windshield Wiper Status"
    )
    sensor_park = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Sensor Park Availability"
    )
    sensor_park_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Sensor Park Status"
    )

    ambient_air = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Ambient Air Availability"
    )
    ambient_air_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Ambient Air Status"
    )

    rear_camera = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Rear Camera Availability"
    )
    rear_camera_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Rear Camera Status"
    )

    screen = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Screen Availability"
    )
    screen_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Screen Status"
    )

    air_condition = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Air Condition Availability"
    )
    air_condition_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Air Condition Status"
    )

    electric_seat = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Electric Seat Availability"
    )
    electric_seat_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Electric Seat Status"
    )

    mirror_folding = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Mirror Folding Availability"
    )
    mirror_folding_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Mirror Folding Status"
    )

    centre_lock = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Centre Lock Availability"
    )
    centre_lock_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Centre Lock Status"
    )

    headlight = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Headlight Availability"
    )
    headlight_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Headlight Status"
    )

    rear_light = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Rear Light Availability"
    )
    rear_light_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Rear Light Status"
    )

    heating_seat = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Heating Seat Availability"
    )
    heating_seat_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Heating Seat Status"
    )

    rear_windshield_wiper = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Rear Windshield Wiper Availability"
    )
    rear_windshield_wiper_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Rear Windshield Wiper Status"
    )

    interior_condition = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Interior Condition Availability"
    )
    interior_condition_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Interior Condition Status"
    )

    dashboard_condition = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Dashboard Condition Availability"
    )
    dashboard_condition_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Dashboard Condition Status"
    )

    side_support = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Side Support Availability"
    )
    side_support_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Side Support Status"
    )

    seat_belts = fields.Selection(
        [('available', 'متوفر'), ('not_available', 'غير متوفر')],
        string="Seat Belts Availability"
    )
    seat_belts_status = fields.Selection(
        [('works', 'يعمل'), ('not_working', 'لا يعمل')],
        string="Seat Belts Status"
    )

    # Engine and Transmission
    engine_condition = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="كبس المحرك"
    )
    engine_seal = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="حالة المحرك العامة"
    )
    oil_leak = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="تسريب زيوت"
    )
    periodic_maintenance = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="صيانة الدورية"
    )
    cooling_system = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="دورة مياه تبريد"
    )
    ac_system = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="دورة التكييف"
    )
    gearbox_test = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="فحص الفتيس"
    )
    chassis_general_condition = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="حالة العامة للعفشة"
    )
    brake_cycle_test = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="فحص دورة الفرامل"
    )
    front_shock_absorbers = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="المساعدين الأمامي"
    )
    rear_shock_absorbers = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="المساعدين الخلفي"
    )
    mounts_condition = fields.Selection(
        [('good', 'جيد'), ('acceptable', 'مقبول'), ('needs_change', 'يحتاج إلى تغيير')],
        string="حالة القواعد – الجلب"
    )
    any_note = fields.Text(string="ملاحظات", required=False, )

    # Suspension

    notes_test_drive = fields.Text(string="ملاحظات أثناء تجربة القيادة")
    attach_diagnostic_report = fields.Many2many(
        'ir.attachment',
        'crm_lead_attach_diagnostic_report_rel',  # Relation table name
        'lead_id',  # Column for this model
        'attachment_id',  # Column for the related model
        string="تقرير فحص جهاز الأعطال",
        help='تقرير فحص جهاز الأعطال.'
    )
    inspection_table = fields.One2many('crm.lead.inspection', 'lead_id', string="جدول الفحص")
    attach_notes_images = fields.Many2many(
        'ir.attachment',
        'crm_lead_attach_notes_images_rel',  # Relation table name
        'lead_id',  # Column for this model
        'attachment_id',  # Column for the related model
        string="الصور الخاصة بملاحظات الفحص",
        help='الصور الخاصة بملاحظات الفحص.',
    )
    final_images = fields.Many2many(
        'ir.attachment',
        'crm_lead_final_images_rel',  # Relation table name
        'lead_id',  # Column for this model
        'attachment_id',  # Column for the related model
        string="الصور النهائية",
        help='الصور النهائية',
    )
    final_video = fields.Many2many(
        'ir.attachment',
        'crm_lead_final_video_rel',  # Relation table name
        'lead_id',  # Column for this model
        'attachment_id',  # Column for the related model
        string="فيديو",
        help='فيديو',
    )
    license_received = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="هل تم استلام الرخصة",
    )
    keys_received = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="هل تم استلام المفاتيح",
    )
    # is_crm_stage = fields.Boolean(compute="compute_crm_individual", default=False)
    #
    #
    # @api.depends('company_type')
    # def compute_crm_individual(self):
    #     for rec in self:
    #         rec.is_crm_individual = True if self.env.user.has_group('sales_enhancement.group_crm_user') \
    #                                         and rec.company_type == 'person' else False

    @api.constrains('final_images', 'final_video', 'stage_id', 'stage_id.sequence')
    def check_ir_attachment_finale_attach(self):
        for rec in self:
            if rec.stage_seq == 7:
                if not rec.final_images or not rec.final_video:
                    raise ValidationError("الصور النهائيه  او الفيديو.")

    @api.constrains('license_front_image', 'license_back_image', 'power_of_attorney_receipt_image', 'additional_image',
                    'owner_id_card_image', 'maintenance_invoices_image', 'license_inquiry_image',
                    'power_of_attorney_image', 'stage_id', 'stage_id.sequence')
    def check_ir_attachment_image(self):
        for rec in self:
            if rec.stage_seq == 4:
                if not rec.license_front_image or not rec.license_back_image or not rec.power_of_attorney_receipt_image or not rec.additional_image or not rec.owner_id_card_image or not rec.maintenance_invoices_image or not rec.license_inquiry_image or not rec.power_of_attorney_image:
                    raise ValidationError("ادخل جميع الصور")

    @api.constrains('attach_notes_images', 'attach_diagnostic_report', 'stage_id', 'stage_id.sequence')
    def check_ir_attachment(self):
        for rec in self:
            if rec.stage_seq == 6:
                if not rec.attach_notes_images or not rec.attach_diagnostic_report:
                    raise ValidationError("الصور الخاصة  او تقرير فحص  لم يوضع.")

    # @api.constrains('attach_notes_images')
    # def check_ir_attachment(self):
    #     print('stage_seq', self.stage_seq)
    #     for rec in self:
    #         if rec.stage_seq == 5:
    #             if not rec.attach_notes_images:
    #                 raise ValidationError("الصور الخاصة لم توضع.")

    def compute_stage_seq(self):
        for rec in self:
            rec.stage_seq = rec.stage_id.sequence

    @api.depends('partner_id')
    def _compute_first_stage(self):
        for rec in self:
            first_stage = self.env['crm.stage'].search([], order='sequence', limit=1)
            rec.first_stage_id = first_stage.id if first_stage else False

    @api.depends('stage_id', 'first_stage_id')
    def _compute_is_first_stage(self):
        for rec in self:
            rec.is_first_stage = rec.stage_id.id == rec.first_stage_id.id

    def action_reset_to_first_stage(self):
        for rec in self:
            if not rec.first_stage_id:
                raise ValidationError("No first stage is defined for this team.")
            rec.stage_id = rec.first_stage_id.id

    @api.depends('stage_id')
    def compute_button_invisible(self):
        next_stage = self.env['crm.stage'].search([('sequence', '>', self.stage_id.sequence)], limit=1)
        for rec in self:
            if not next_stage:
                rec.button_invisible = True
            else:
                rec.button_invisible = False

    @api.depends('stage_id')
    def compute_previous_stage(self):
        previous_stage = self.env['crm.stage'].search([('sequence', '<', self.stage_id.sequence)],
                                                      order='sequence desc', limit=1)
        for rec in self:
            if not previous_stage:
                rec.previous_stage = True
            else:
                rec.previous_stage = False

    def action_accept(self):
        next_stage = self.env['crm.stage'].search([('sequence', '>', self.stage_id.sequence)], limit=1)
        if not next_stage:
            raise ValidationError('No next stage available.')
        self.write({'stage_id': next_stage.id})
        return True

    def action_previous(self):
        previous_stage = self.env['crm.stage'].search([('sequence', '<', self.stage_id.sequence)],
                                                      order='sequence desc', limit=1)
        if not previous_stage:
            raise ValidationError('No previous stage available.')
        self.write({'stage_id': previous_stage.id})
        return True

    # @api.constrains('type', 'cus_name', 'cus_phone', 'cus_region', 'cus_source', 'project_name', 'communication_method')
    # def _check_required_fields(self):
    #     for record in self:
    #         if record.type == 'lead':
    #             if not all(
    #                     [record.cus_name, record.cus_phone, record.cus_region, record.cus_source, record.project_name,
    #                      record.communication_method]):
    #                 raise ValidationError("All required fields must be filled when type is 'Lead'.")
    #
