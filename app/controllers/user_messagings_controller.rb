class UserMessagingsController < ApplicationController
  before_action :set_user_messaging, only: [:show, :edit, :update, :destroy]

  # GET /user_messagings
  def index
    @q = UserMessaging.ransack(params[:q])
    @user_messagings = @q.result(:distinct => true).includes(:recipient, :product).page(params[:page]).per(10)
  end

  # GET /user_messagings/1
  def show
  end

  # GET /user_messagings/new
  def new
    @user_messaging = UserMessaging.new
  end

  # GET /user_messagings/1/edit
  def edit
  end

  # POST /user_messagings
  def create
    @user_messaging = UserMessaging.new(user_messaging_params)

    if @user_messaging.save
      message = 'UserMessaging was successfully created.'
      if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
        redirect_back fallback_location: request.referrer, notice: message
      else
        redirect_to @user_messaging, notice: message
      end
    else
      render :new
    end
  end

  # PATCH/PUT /user_messagings/1
  def update
    if @user_messaging.update(user_messaging_params)
      redirect_to @user_messaging, notice: 'User messaging was successfully updated.'
    else
      render :edit
    end
  end

  # DELETE /user_messagings/1
  def destroy
    @user_messaging.destroy
    message = "UserMessaging was successfully deleted."
    if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
      redirect_back fallback_location: request.referrer, notice: message
    else
      redirect_to user_messagings_url, notice: message
    end
  end


  private
    # Use callbacks to share common setup or constraints between actions.
    def set_user_messaging
      @user_messaging = UserMessaging.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def user_messaging_params
      params.require(:user_messaging).permit(:recipient_id, :sender_id, :message_data, :product_id)
    end
end
