import os
import glob
import time
from datetime import datetime, timedelta
from typing import List
from consumer_utils.logger import setup_logger
from core.config_sample import settings

logger = setup_logger(__name__)

class LogCleanup:
    def __init__(self, log_dir: str = "logs", days_to_keep: int = None):
        self.log_dir = log_dir
        self.days_to_keep = days_to_keep or settings.LOG_CLEANUP_DAYS
        self.logger = setup_logger(__name__)

    def get_old_log_files(self) -> List[str]:
        """Get list of log files older than the specified days"""
        current_time = time.time()
        old_files = []
        
        # Get all log files in the directory
        log_files = glob.glob(os.path.join(self.log_dir, "*.log"))
        
        for log_file in log_files:
            # Get file modification time
            file_time = os.path.getmtime(log_file)
            # Calculate age in days
            age_in_days = (current_time - file_time) / (24 * 3600)
            
            if age_in_days > self.days_to_keep:
                old_files.append(log_file)
                
        return old_files

    def cleanup_old_logs(self) -> None:
        """Remove log files older than the specified days"""
        if not settings.LOG_CLEANUP_ENABLED:
            self.logger.info("Log cleanup is disabled")
            return

        try:
            old_files = self.get_old_log_files()
            
            if not old_files:
                self.logger.info("No old log files found to clean up")
                return

            for file_path in old_files:
                try:
                    os.remove(file_path)
                    self.logger.info(f"Deleted old log file: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error deleting log file {file_path}: {str(e)}")

            self.logger.info(f"Log cleanup completed. Removed {len(old_files)} files")
            
        except Exception as e:
            self.logger.error(f"Error during log cleanup: {str(e)}")
            raise

    def cleanup_unidentified_messages(self) -> None:
        """Clean up unidentified messages log file"""
        unidentified_file = os.path.join(self.log_dir, "unidentified_messages.log")
        
        if os.path.exists(unidentified_file):
            try:
                # Create backup with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"{unidentified_file}.{timestamp}"
                os.rename(unidentified_file, backup_file)
                
                # Create new empty file
                open(unidentified_file, 'a').close()
                
                self.logger.info("Unidentified messages log file cleaned up")
            except Exception as e:
                self.logger.error(f"Error cleaning up unidentified messages: {str(e)}")
                raise

def cleanup_logs() -> None:
    """Main function to perform log cleanup"""
    cleanup = LogCleanup()
    cleanup.cleanup_old_logs()
    cleanup.cleanup_unidentified_messages() 