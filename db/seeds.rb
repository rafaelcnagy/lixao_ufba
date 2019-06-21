# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
subject_list = [
  [ 'ENGENHARIA DE SOFTWARE I', 'MATA62', 'Ementa' ],
  [ 'COMPILADORES', 'MATA61', 'Ementa' ],
  [ 'PARADIGMAS DE LINGUAGENS DE PROGRAMAÇÃO', 'MATA56', 'Ementa' ],
  [ 'LÓGICA PARA COMPUTAÇÃO', 'MATA47', 'Ementa' ],
  [ 'METODOLOGIA E EXPRESSÃO TÉCNICO-CIENTÍFICA', 'FCHC45', 'Ementa' ]
]

subject_list.each do |name, code, about|
	Subject.create( name: name, code: code, about: about )
end


class_subject_list = [
	[ '020200', '14:50', '16:40' ],
	[ '010100', '16:40', '18:30' ],
	[ '020200', '13:00', '14:50' ],
	[ '010100', '16:40', '18:30' ],
	[ '010000', '14:50', '16:40' ]
]

class_subject_list.each do |number, hour_begins, hour_ends|
	ClassSubject.create( number: number, hour_begins: hour_begins, hour_ends: hour_ends )
end


students_list = [
	[ 'Rafael', 216220012, 216220012 ],
	[ 'Vinícius', 151235, 151235],
	[ 'Jorel', 10241, 10241],
	[ 'Irmão do Jorel', 1511111, 1511111]
]

students_list.each do |name, cpf, registry|
	Student.create( name: name, cpf: cpf, registry: registry )
end

