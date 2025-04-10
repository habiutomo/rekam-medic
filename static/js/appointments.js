document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('appointmentCalendar');
    
    if (calendarEl) {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            themeSystem: 'bootstrap5',
            headerToolbar: {
                left: 'prevYear,prev,next,nextYear today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
            },
            buttonText: {
                today: 'Today',
                month: 'Month',
                week: 'Week',
                day: 'Day',
                list: 'List'
            },
            navLinks: true,
            editable: true,
            dayMaxEvents: true,
            events: '/appointments/json',
            eventClick: function(info) {
                window.location.href = `/appointments/view/${info.event.id}`;
            },
            dateClick: function(info) {
                window.location.href = `/appointments/new?date=${info.dateStr}`;
            },
            eventContent: function(arg) {
                let time = '';
                if (arg.event.start) {
                    time = arg.event.start.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                }
                
                const title = arg.event.title || 'Unnamed Appointment';
                const status = arg.event.extendedProps.status || 'scheduled';
                
                let statusClass = '';
                switch(status) {
                    case 'scheduled':
                        statusClass = 'bg-success';
                        break;
                    case 'completed':
                        statusClass = 'bg-primary';
                        break;
                    case 'cancelled':
                        statusClass = 'bg-danger';
                        break;
                    case 'no-show':
                        statusClass = 'bg-warning';
                        break;
                }
                
                const patientName = arg.event.extendedProps.patient || '';
                const doctorName = arg.event.extendedProps.doctor || '';
                
                return { 
                    html: `
                        <div class="fc-event-time">${time}</div>
                        <div class="fc-event-title-container">
                            <div class="fc-event-title">${title}</div>
                            <div class="fc-event-title">${patientName}</div>
                            <div class="small badge ${statusClass}">${status}</div>
                        </div>
                    `
                };
            },
            eventTimeFormat: {
                hour: '2-digit',
                minute: '2-digit',
                meridiem: false,
                hour12: false
            }
        });
        
        calendar.render();
        
        // Connect to navigation buttons
        document.getElementById('prevButton').addEventListener('click', function() {
            calendar.prev();
        });
        
        document.getElementById('nextButton').addEventListener('click', function() {
            calendar.next();
        });
        
        document.getElementById('todayButton').addEventListener('click', function() {
            calendar.today();
        });
    }
});