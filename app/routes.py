from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import db, Event, TeamMember
from .forms import EventForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    q = request.args.get('q', '').strip()
    if q:
        # Search by title, description, location, organizer (case-insensitive)
        events = Event.query.filter(
            db.or_(
                Event.title.ilike(f'%{q}%'),
                Event.description.ilike(f'%{q}%'),
                Event.location.ilike(f'%{q}%'),
                Event.organizer.ilike(f'%{q}%')
            )
        ).order_by(Event.date).all()
    else:
        events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)

@bp.route('/event/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    return render_template('event_detail.html', event=event)


@bp.route('/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            organizer=form.organizer.data,
            budget=form.budget.data or 0.0,
            details=form.details.data
        )
        db.session.add(event)
        db.session.flush()
        for member_form in form.team_members:
            if member_form.name.data:
                member = TeamMember(
                    name=member_form.name.data,
                    contact=member_form.contact.data,
                    role=member_form.role.data,
                    event_id=event.id
                )
                db.session.add(member)
        db.session.commit()
        flash('Event created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_event.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if request.method == 'GET':
        for member in event.team_members:
            form.team_members.append_entry({
                'name': member.name,
                'contact': member.contact,
                'role': member.role
            })
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.location = form.location.data
        event.organizer = form.organizer.data
        event.budget = form.budget.data or 0.0
        event.details = form.details.data
        TeamMember.query.filter_by(event_id=event.id).delete()
        for member_form in form.team_members:
            if member_form.name.data:
                member = TeamMember(
                    name=member_form.name.data,
                    contact=member_form.contact.data,
                    role=member_form.role.data,
                    event_id=event.id
                )
                db.session.add(member)
        db.session.commit()
        flash('Event updated!', 'success')
        return redirect(url_for('main.event_detail', id=event.id))
    return render_template('edit_event.html', form=form, event=event)


@bp.route('/delete/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'warning')
    return redirect(url_for('main.index'))