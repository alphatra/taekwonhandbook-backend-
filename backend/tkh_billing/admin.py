from django.contrib import admin

from .models import AdPolicy, Club, ClubMember, Entitlement, Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price_cents", "currency", "trial_days")
    search_fields = ("code", "name")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "provider", "status", "current_period_end", "seats")
    list_filter = ("provider", "status")
    search_fields = ("external_id", "user__username")


@admin.register(Entitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "active", "updated_at")
    list_filter = ("key", "active")
    search_fields = ("user__username",)


class ClubMemberInline(admin.TabularInline):
    model = ClubMember
    extra = 0


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "plan", "seats_total", "seats_used")
    search_fields = ("name", "owner__username")
    inlines = [ClubMemberInline]


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ("club", "user", "role")
    list_filter = ("role",)
    search_fields = ("club__name", "user__username")


@admin.register(AdPolicy)
class AdPolicyAdmin(admin.ModelAdmin):
    list_display = ("user", "today_shown", "session_shown", "daily_cap", "session_cap", "last_shown_at")
    search_fields = ("user__username",)

