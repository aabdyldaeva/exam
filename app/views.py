import datetime

from flask import render_template, request, redirect, url_for, flash
from . import app, db
from .models import Position, Employee
from .forms import PositionForm, EmployeeForm


def index():
    title = 'List of employees'
    employees = Employee.query.all()
    return render_template('index.html', employees=employees, title=title)


def position_create():
    title = 'Add position'
    form = PositionForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_position = Position()
            form.populate_obj(new_position)
            db.session.add(new_position)
            db.session.commit()
            flash(f'Position # {new_position.id} successfully added', 'success')
            return redirect(url_for('employees'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in the field  {field} , error text: {error}', 'danger')
    return render_template('position_form.html', form=form, title=title)


def position_update(position_id):
    position = Position.query.filter_by(id=position_id).first()
    form = PositionForm(request.form, obj=position)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(position)
            db.session.commit()
            flash(f'Position # {position_id} updated')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in the {field}, error text :  {error}', 'danger')
    return render_template('position_form.html', form=form, position=position)


def position_delete(position_id):
    position = Position.query.filter_by(id=position_id).first()
    form = PositionForm()
    if request.method == 'GET':
        return render_template('position_delete.html', position=position, form=form)
    if request.method == 'POST':
        db.session.delete(position)
        db.session.commit()
        return redirect(url_for('position_create'))


def employee_create():
    title = 'Add employee'
    form = EmployeeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_employee= Employee()
            form.populate_obj(new_employee)
            db.session.add(new_employee)
            db.session.commit()
            flash(f'Employee # {new_employee.id} added to the list', 'success')
            return redirect(url_for('employees'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in the  {field} , error text {error}', 'danger')
    return render_template('employee_form.html', form=form, title=title)


def employee_detail(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    return render_template('employee_detail.html', employee=employee)


def employee_update(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    form = EmployeeForm(request.form, obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.commit()
            flash(f'Employee # {employee_id} updated', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in the  {field} , error text {error}', 'danger')
    return render_template('employee_form.html', form=form, employee=employee)


def employee_delete(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    form = EmployeeForm()
    if request.method == 'GET':
        return render_template('employee_delete.html', employee=employee, form=form)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('employees'))
