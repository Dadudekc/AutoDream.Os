# Widget Configuration Manual QA

Steps to verify widget customization:

1. **Open the Dashboard**
   - Generate the dashboard HTML using `DashboardFrontend` or open an existing dashboard page.
2. **Open Configuration Dialog**
   - Click the ⚙ icon on any widget.
   - A configuration modal should appear.
3. **Modify Settings**
   - Change the widget title, refresh interval, width, and height.
4. **Save Configuration**
   - Click **Save**. The widget should update immediately.
5. **Verify Persistence**
   - Refresh the page.
   - Confirm that the widget retains the updated settings, indicating they were stored in `localStorage`.
