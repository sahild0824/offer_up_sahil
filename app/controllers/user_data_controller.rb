class UserDataController < ApplicationController
  before_action :set_user_datum, only: [:show, :edit, :update, :destroy]

  # GET /user_data
  def index
    @user_data = UserDatum.all
  end

  # GET /user_data/1
  def show
  end

  # GET /user_data/new
  def new
    @user_datum = UserDatum.new
  end

  # GET /user_data/1/edit
  def edit
  end

  # POST /user_data
  def create
    @user_datum = UserDatum.new(user_datum_params)

    if @user_datum.save
      redirect_to @user_datum, notice: 'User datum was successfully created.'
    else
      render :new
    end
  end

  # PATCH/PUT /user_data/1
  def update
    if @user_datum.update(user_datum_params)
      redirect_to @user_datum, notice: 'User datum was successfully updated.'
    else
      render :edit
    end
  end

  # DELETE /user_data/1
  def destroy
    @user_datum.destroy
    redirect_to user_data_url, notice: 'User datum was successfully destroyed.'
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_user_datum
      @user_datum = UserDatum.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def user_datum_params
      params.require(:user_datum).permit(:username, :password, :email_address)
    end
end
