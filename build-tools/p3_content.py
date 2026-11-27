# -*- coding: utf-8 -*-
"""Project 3: The Hair Patch Studio copy mapped onto the Hairise theme. Facts from thehairpatchstudio.com."""
from p2_content import PHONE, TEL, EMAIL, ADDRESS, MAPS, REV

IG = 'https://www.instagram.com/hairpatchlondon/'
WA = 'https://wa.me/447404902708'

INTRO = ('At The Hair Patch Studio, we provide advanced non-surgical hair replacement solutions designed '
         'for a completely natural look.')
FOOTER = 'Specialist hair patch experts based in the UK — advanced non-surgical hair replacement for a completely natural look.'

# Hairise reuses the same placeholder in many slots: map those by occurrence (per page).
L_SHORT = 'Vestibulum morbi blandit cursus risus. Augue neque gravida in fermentum et sollicitudin.'
L_STAT = 'Vestibulum morbi blandit cursus risus. Augue neque gravida.'
L_CARD = 'Vestibulum morbi blandit cursus risus. Augue neque gravida in fermentum et sollicitudin ac orci phasellus. Massa massa ultricies mi quis hendrerit.'
L_QUOTE = 'Vestibulum morbi blandit cursus risus. Augue neque gravida in fermentum et sollicitudin ac orci phasellus. Massa massa ultricies mi quis hendrerit Vestibulum morbi blandit cursus risus. Augue neque gravida.'
L_MED = 'Vestibulum morbi blandit cursus risus. Augue neque gravida in fermentum et sollicitudin ac orci phasellus.'
L_TINY = 'Vestibulum morbi blandit cursus risus.'

SEQ = {
    'index.html': {
        L_SHORT: [INTRO + ' Our expert technicians ensure precision fitting, comfort, and long-lasting results.'],
        L_STAT: ['Clients who have regained their confidence with us.',
                 'Years of hands-on experience in non-surgical hair replacement.',
                 'Professional awards for quality, hygiene and results.'],
        L_CARD: ['Every system is tailored to your hair texture, density and personal style, with seamless blending for a finish no one can spot.',
                 'Customised hair systems matched to your hair density, colour and style — designed with attention to detail for a flawless result.',
                 'Comfortable glue, tape and clip-on bonding options that stay secure, with professional maintenance to keep them that way.'],
        L_QUOTE: [REV['Binay'], REV['Prashant'], REV['Dhaval']],
        L_MED: ['A one-to-one consultation to assess your hair loss and find the right non-surgical solution for you.',
                'Professional cleaning, rebonding and refitting to keep your hair system secure, hygienic and long-lasting.'],
    },
    'about.html': {
        'Transplant': ['Fitting', 'Bonding'],
        L_CARD: ['We are a trusted specialist studio offering premium non-surgical hair replacement solutions across the UK. Our customised hair systems are carefully designed to deliver natural appearance, comfort, and long-term durability.'],
        L_STAT: ['We offer high-quality hair solution services, tailored to match your hair texture, density and personal style.',
                 'Focus on cleanliness & maintenance, spreading happiness through all we do, and keeping creativity and artistry at their best.'],
        L_QUOTE: [REV['Binay'], REV['Prashant'], REV['Dhaval']],
    },
    'services.html': {
        L_STAT: ['We assess your hair loss, texture, density and style in a one-to-one consultation.',
                 'Your system is designed to match your colour, density and natural hairline.',
                 'Expert installation with secure bonding and seamless blending for a natural finish.',
                 'Professional cleaning, rebonding and refitting keep your system secure and hygienic.'],
        L_SHORT: ['Popular and in-demand non-surgical hair patch solutions, each designed for a flawless, undetectable finish.'],
    },
}
DEFAULT = {L_SHORT: FOOTER, L_TINY: 'Is there anything else you need help with? Just get in touch with us.'}

# per-page overrides for strings that mean different things on different pages
PAGE_TEXT = {
    'about.html': {
        'Welcome to our Hair Transplant Center': 'Who are we?',
        'OUR SPECIALIST': 'OUR STUDIO', 'Meet our Scientists': 'Meet our specialists',
        'Heir Specialist': 'Precision fitting & blending', 'Founder Director': 'Custom-made systems',
        'Genetic Specialist': 'Cleaning & refitting', 'Hair Testing': 'Crown volume & toppers',
        'Lopes Mads': 'Topper specialists',
        'TECHNICAL DIRECTOR': 'GOOGLE REVIEW', 'FOUNDER DIRECTOR': 'GOOGLE REVIEW', 'SENIOR TECHNICIAN': 'GOOGLE REVIEW',
    },
    'services.html': {
        'Hair Loss Solutions': 'Free consultation', 'Amazing results, every time': 'Your custom hair system',
        'Natural Looking Results': 'Precision fitting', 'International Standards': 'Aftercare & maintenance',
    },
}
# names that are team members in one slot and reviewers in another (about page): by occurrence
NAME_SEQ = {
    'about.html': {'Simon Amour': ['Hair patch technicians', 'Binay Singh'], 'Robbie Lee': ['Hair system designers', 'Prashant Mohite'],
                   'Emma Aria': ['Maintenance specialists', 'Dhaval Solanki']},
}

TEXT = {
    # header / offcanvas / menus
    '+91-234-567-8900': PHONE, '+123 456 789': PHONE, '(000) 123456789': PHONE,
    'themeht23@gmail.com': EMAIL,
    'Appointment': 'Free Consultation',
    'Pages': 'About',
    "Let's Get In Touch": "Let's Get In Touch",
    'Genetic Testing': 'Hair Patch Fixing', 'Food Sensitivity': 'Custom Hair System Design',
    'Quality Control': 'Glue & Tape Bonding', 'Vaccine innovation': 'Maintenance & Refitting',
    'Select Service': 'Select Service',
    'Hair Loss Diagnosis': 'Hair Patch Fixing', 'Androgenetic Alopecia': 'Glue Bond Hair System',
    'Prosthetic Hair': 'Tape Bond Hair System', 'Beard Restoration': 'Clip-On Hair System',
    'Body Hair Transplant': 'Hair Topper Solutions', 'Hair Reconstruction': 'Hair System Maintenance',
    'Contact us': 'Contact us',

    # home
    'Hairise – Hair Transplantation and Hair Removal WordPress': 'The Hair Patch Studio – Non-Surgical Hair Replacement, London',
    'Technique of Hair Transplant': 'Non-surgical hair replacement',
    'Destination for': 'Specialist Hair', 'Hair Restoration': 'Patch Experts, UK',
    'Hair Transplant': 'Natural Look,', 'Proven Results': 'Real Confidence',
    'transplant': 'fitting', 'Hair Loss Medication': 'Hair Patch Fixing',
    'regrowth': 'design', 'Dandruff Treatment': 'Custom Hair Systems',
    'treatment': 'bonding', 'Advanced Treatment': 'Glue & Tape Bonding',
    'research': 'care', 'Pattern Baldness': 'Maintenance & Refitting',
    'Better For You': 'Why Choose Us',
    'Welcome to our Hair Transplant Center': 'Welcome to The Hair Patch Studio',
    'Best Clinic for safe Procedure': 'Specialists in non-surgical hair replacement',
    'Advanced Non-touch Bio FUE': 'Natural & undetectable finish',
    'about us': 'about us',
    '100%': '1561+', 'Report Efficiency': 'Happy Customers',
    '200k': '10', 'Complete Cases': 'Years In Business',
    '650+': '9', 'Our Equipment': 'Professional Awards',
    'Hair Loss Solutions': 'Natural & undetectable',
    'Amazing results, every time': 'Custom-made hair systems',
    'Natural Looking Results': 'Comfortable & secure bonding',
    'Hairgrowth Cycle': 'Why choose us', 'Types Of Hair Loss': 'Our values',
    'Affordable Prices': 'One-to-one consultation', 'Advanced Techniques': 'Custom-made systems',
    'International Standards': 'Focus on cleanliness', 'Life Long Results': 'Natural, lasting results',
    'Service We Provide': 'Non-Surgical Hair Replacement',
    'Clinical Research': 'Fitting', 'Hair Loss': 'Bonding', 'Transplant': 'Bonding', 'Hair Research': 'Flexible',
    'RESEARCH': 'TRANSFORMATIONS', 'Latest From Case Studies': 'See Our Transformations',
    'Healthier Hair': 'Before & After', 'Afro Hair Transplantation': 'Full hair patch transformation',
    'DHT': 'Before & After', 'PRP Treatment For Hair': 'Natural hairline restored',
    'Follicular Unit Extraction': 'A complete new look',
    'Some select projects that showcase.': 'Natural results achieved through our non-surgical hair replacement solutions.',
    'View all': 'More on Instagram',
    'Simon Amour': 'Binay Singh', 'Robbie Lee': 'Prashant Mohite', 'Emma Aria': 'Dhaval Solanki',
    'Technical Director': 'Google review', 'Genetic specialist': 'Google review',
    'Advanced Dandruff Treatment': 'Hair System Maintenance',
    'our blog': 'aftercare', 'Explore our Latest Post': 'Care That Keeps Your System Perfect',
    'admin': 'The Hair Patch Studio',
    'Multivitamins and Hair Loss: The Ultimate Truth': 'Hair system maintenance',
    'Hair Care': 'Aftercare',
    'Does Eyelash Grow Back: Dermatologist Answers': 'Hair patch cleaning & refitting',
    'What is Implanter Pen in DHT Hair Transplant?': 'Hair topper solutions',

    # footer
    'Newsletter': 'Free Consultation',
    '5th Street, New York, USA': ADDRESS,
    'Quick Links': 'Quick Links', 'Team Member': 'Our Specialists', 'Our History': 'Our Mission', 'Faq': 'Contact Us',
    'Resource': 'Reach Us',
    'Privacy Policy': 'Call ' + PHONE, 'Terms And Conditions': 'WhatsApp', 'Career': 'Instagram',
    'How We Work': 'Email us', 'Knowledge Base': 'Find the studio',
    'Copyright © 2024 All Rights Reserved | Hairise Made by ThemeHt.': 'Copyright © 2026 The Hair Patch Studio | All Rights Reserved.',

    # about
    'About Us – Hairise': 'About Us – The Hair Patch Studio',
    'ABOUT US': 'ABOUT US', 'PRP THERAPY': 'OUR MISSION', 'STRIP HARVESTING': 'OUR VALUES',
    'Regrowth': 'Design', 'Treatment': 'Bonding',

    # services
    'Hair Loss Diagnosis – Hairise': 'Services – The Hair Patch Studio',
    'orbi porta dolor quis sem ultricies maximus. Nunc accumsan dui vel lobortis pulvinar. Duis convallis odio ut dignissim faucibus. Sed sit amet urna dictum, interdum justo sed, lacinia dolor. Phasellus finibus nunc id tellus mollis consequat. Maecenas ornare aliquet vestibulum. Integer leo magna, viverra a imperdiet id, vehicula non mi. Vestibulum nec arcu dolor.':
        'e provide professional non-surgical hair patch solutions, including custom systems, secure bonding, and maintenance services. Our expert technicians ensure precision fitting, comfort, and long-lasting results — helping you regain confidence instantly.',
    'Our Procedures': 'How It Works',
    'Nunc accumsan dui vel lobortis pulvinar. Duis convallis odio ut dignissim faucibus. Sed sit amet urna dictum, interdum justo sed, lacinia dolor. Phasellus finibus nunc id tellus mollis consequat. Maecenas ornare aliquet vestibulum.':
        'From your first consultation to the final fitting, every step is discreet, comfortable and tailored to you.',
    'Advantages of Hair Transplantation': 'Why Choose a Hair System?',
    'Morbi porta dolor quis sem ultricies maximus. Nunc accumsan dui vel lobortis pulvinar. Duis convallis odio ut dignissim faucibus. Sed sit amet urna dictum, interdum justo sed, lacinia dolor. Phasellus finibus nunc id tellus mollis consequat. Maecenas ornare aliquet vestibulum. Integer leo magna, viverra a imperdiet id, vehicula non mi. Vestibulum nec arcu dolor.':
        'Hair loss can affect self-confidence. A non-surgical hair system restores a full, natural look straight away — no surgery and no downtime. Whether you are experiencing early thinning or advanced hair loss, our team provides a discreet, comfortable and professional experience from consultation to final result.',
    'Screening Plans': 'What We Offer',
    'Nunc accumsan dui vel lobortis pulvinar.': 'Hair patch fixing with precise, natural blending',
    'Duis convallis odio ut dignissim faucibus.': 'Custom hair systems matched to your density and colour',
    'Sed sit amet urna dictum, interdum justo sed.': 'Glue bond systems for maximum hold',
    'Maecenas ornare aliquet vestibulum.': 'Lightweight tape bond systems',
    'Phasellus finibus nunc id tellus mollis consequat.': 'Clip-on systems and hair toppers',
    'Vehicula non mi. Vestibulum nec arcu dolor.': 'Cleaning, rebonding and refitting',
    'Services List': 'Our Services',
    'How Can We Help?': 'Have Other Queries?',

    # contact
    'Contact – Hairise': 'Contact – The Hair Patch Studio',
    'Make an Appointment': 'Book Your Free Consultation',
    'Contact with us': 'Get in touch',
    '24/7 Contact us': 'Call us',
    'Mail us': 'Mail us', 'Address': 'Address',
}
