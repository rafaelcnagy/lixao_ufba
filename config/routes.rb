Rails.application.routes.draw do
  get 'user/index'
  devise_for :users

  root to: 'user#index'

 end
