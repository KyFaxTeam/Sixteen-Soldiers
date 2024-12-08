# logger_config.py
import logging
import traceback
import sys
from pathlib import Path

class AutoExceptionFormatter(logging.Formatter):
    def format(self, record):
        # Format de base
        formatted_message = super().format(record)
        
        # Si c'est une erreur, on capture automatiquement l'exception en cours
        if record.levelno >= logging.ERROR:
            # Si exc_info n'est pas déjà défini, on le récupère
            if not record.exc_info:
                record.exc_info = sys.exc_info()
            
            # Si on a une exception
            if record.exc_info and record.exc_info != (None, None, None):
                exc_type, exc_value, exc_traceback = record.exc_info
                
                # Obtenir le traceback complet
                tb_list = traceback.extract_tb(exc_traceback)
                if tb_list:  # Vérifier qu'on a bien un traceback
                    original_error = tb_list[0]
                    origin_path = Path(original_error.filename)
                    
                    error_details = (
                        f"\n─────────── Details ───────────"
                        f"\n➤ Error Origin: {origin_path.name}:{original_error.lineno}"
                        f"\n➤ Error Function: {original_error.name}"
                        f"\n➤ Error Line: {original_error.line}"
                        f"\n➤ Error Type: {exc_type.__name__}"
                        f"\n➤ Error Message: {str(exc_value)}"
                        f"\n─────────── Caught At ───────────"
                        f"\n➤ Logger: {record.name}"
                        f"\n➤ Caught in: {Path(record.pathname).name}:{record.lineno}\n"
                        
                    )
                    return formatted_message + error_details
        
        return formatted_message

def setup_logging(level=logging.INFO):
    # Supprime les handlers existants pour éviter les doublons
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # Configuration du handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter personnalisé qui capture automatiquement les exceptions
    formatter = AutoExceptionFormatter(
        # fmt='\n%(levelname)s - %(asctime)s - %(name)s\n%(message)s'
        fmt='\n%(levelname)s - %(message)s'
    )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)

def get_logger(name):
    """
    Récupère un logger configuré pour un module spécifique.
    """
    return logging.getLogger(name)