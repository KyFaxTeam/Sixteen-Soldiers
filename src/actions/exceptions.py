class DeplacementInvalideError(Exception):
    """Exception levée lorsqu'un déplacement de pion est invalide."""
    pass

class CaptureInvalideError(Exception):
    """Exception levée lorsqu'une capture de pion est invalide."""
    pass

class PartieTermineeError(Exception):
    """Exception levée lorsqu'une action est effectuée sur une partie terminée."""
    pass