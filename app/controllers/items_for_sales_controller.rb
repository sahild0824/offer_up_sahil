class ItemsForSalesController < ApplicationController
  before_action :set_items_for_sale, only: [:show, :edit, :update, :destroy]

  # GET /items_for_sales
  def index
    @q = ItemsForSale.ransack(params[:q])
    @items_for_sales = @q.result(:distinct => true).includes(:product, :seller).page(params[:page]).per(10)
  end

  # GET /items_for_sales/1
  def show
  end

  # GET /items_for_sales/new
  def new
    @items_for_sale = ItemsForSale.new
  end

  # GET /items_for_sales/1/edit
  def edit
  end

  # POST /items_for_sales
  def create
    @items_for_sale = ItemsForSale.new(items_for_sale_params)

    if @items_for_sale.save
      message = 'ItemsForSale was successfully created.'
      if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
        redirect_back fallback_location: request.referrer, notice: message
      else
        redirect_to @items_for_sale, notice: message
      end
    else
      render :new
    end
  end

  # PATCH/PUT /items_for_sales/1
  def update
    if @items_for_sale.update(items_for_sale_params)
      redirect_to @items_for_sale, notice: 'Items for sale was successfully updated.'
    else
      render :edit
    end
  end

  # DELETE /items_for_sales/1
  def destroy
    @items_for_sale.destroy
    message = "ItemsForSale was successfully deleted."
    if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
      redirect_back fallback_location: request.referrer, notice: message
    else
      redirect_to items_for_sales_url, notice: message
    end
  end


  private
    # Use callbacks to share common setup or constraints between actions.
    def set_items_for_sale
      @items_for_sale = ItemsForSale.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def items_for_sale_params
      params.require(:items_for_sale).permit(:seller_name, :product_id, :product_description, :price, :product_category)
    end
end
