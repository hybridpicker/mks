"""
Management command to check and enforce 2FA setup
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Check 2FA status and enforce setup for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-all',
            action='store_true',
            help='Force all users to setup 2FA',
        )
        parser.add_argument(
            '--staff-only',
            action='store_true',
            help='Only enforce 2FA for staff users',
        )
        parser.add_argument(
            '--report-only',
            action='store_true',
            help='Only report 2FA status without making changes',
        )

    def handle(self, *args, **options):
        users = User.objects.all()
        
        if options['staff_only']:
            users = users.filter(is_staff=True)
        
        total_users = users.count()
        users_with_2fa = users.filter(is_2fa_enabled=True).count()
        users_without_2fa = users.filter(is_2fa_enabled=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'2FA Status Report:')
        )
        self.stdout.write(f'Total users: {total_users}')
        self.stdout.write(f'Users with 2FA: {users_with_2fa}')
        self.stdout.write(f'Users without 2FA: {users_without_2fa.count()}')
        
        if not options['report_only']:
            self.stdout.write('\nUsers without 2FA:')
            for user in users_without_2fa:
                role = 'Admin' if user.is_superuser else 'Staff' if user.is_staff else 'User'
                self.stdout.write(f'  - {user.username} ({user.email}) [{role}]')
                
                if options['force_all'] or (options['staff_only'] and user.is_staff):
                    # Here you could implement additional enforcement logic
                    # For now, we just report
                    pass
        
        if users_without_2fa.exists() and not options['report_only']:
            self.stdout.write(
                self.style.WARNING(
                    '\nRecommendation: Enable 2FA middleware to enforce setup for new logins.'
                )
            )
