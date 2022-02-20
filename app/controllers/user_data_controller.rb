class UserDataController < ApplicationController
  before_action :set_user_datum, only: %i[show edit update destroy]

  def index
    @q = UserDatum.ransack(params[:q])
    @user_data = @q.result(distinct: true).includes(:seller_id,
                                                    :user_messagings, :items_for_sales).page(params[:page]).per(10)
  end

  def show
    @user_messaging = UserMessaging.new
    @product_description = ProductDescription.new
  end

  def new
    @user_datum = UserDatum.new
  end

  def edit; end

  def create
    @user_datum = UserDatum.new(user_datum_params)

    if @user_datum.save
      redirect_to @user_datum, notice: "User datum was successfully created."
    else
      render :new
    end
  end

  def update
    if @user_datum.update(user_datum_params)
      redirect_to @user_datum, notice: "User datum was successfully updated."
    else
      render :edit
    end
  end

  def destroy
    @user_datum.destroy
    redirect_to user_data_url, notice: "User datum was successfully destroyed."
  end

  private

  def set_user_datum
    @user_datum = UserDatum.find(params[:id])
  end

  def user_datum_params
    params.require(:user_datum).permit(:username, :password, :email_address)
  end
end
