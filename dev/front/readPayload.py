# get name and phone number from the form payload
def parse_payload(data):
    name = data['name']
    phone_number = data['phone_number']

    return (name, phone_number)


def generate_prompt(name):
    return f'''Hey {name}! I am excited to be working for you. I'm here to help take the load off you a little
    bit while watching over your kid.'''
