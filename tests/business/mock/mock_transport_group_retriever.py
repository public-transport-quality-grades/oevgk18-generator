from generator.business.model.public_transport_group import PublicTransportGroup


def calculate_transport_groups(registry):
    return {
        8503400: PublicTransportGroup.A,
        8503125: PublicTransportGroup.B,
        8591382: PublicTransportGroup.C,
        8593245: PublicTransportGroup.A
    }
