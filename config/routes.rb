Rails.application.routes.draw do
  get 'home/index'
  get 'user/index'
  devise_for :users

  root to: 'home#index'

  match '/student/new', to: 'student#create', via: :post
 end
