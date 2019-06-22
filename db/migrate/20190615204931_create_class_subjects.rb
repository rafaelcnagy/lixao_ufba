class CreateClassSubjects < ActiveRecord::Migration[5.2]
  def change
    create_table :class_subjects do |t|
      t.string :number
      t.string :hour_begins

      t.timestamps
    end
  end
end
