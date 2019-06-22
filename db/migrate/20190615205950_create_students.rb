class CreateStudents < ActiveRecord::Migration[5.2]
  def change
    create_table :students do |t|
      t.string :name
      t.integer :cpf
      t.integer :registry

      t.timestamps
    end
  end
end
