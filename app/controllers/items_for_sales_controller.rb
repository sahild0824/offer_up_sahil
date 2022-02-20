class ItemsForSalesController < ApplicationController
  before_action :set_items_for_sale, only: [:show, :edit, :update, :destroy]

  # GET /items_for_sales
  def index
    @items_for_sales = ItemsForSale.all
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
      redirect_to @items_for_sale, notice: 'Items for sale was successfully created.'
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
    redirect_to items_for_sales_url, notice: 'Items for sale was successfully destroyed.'
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
