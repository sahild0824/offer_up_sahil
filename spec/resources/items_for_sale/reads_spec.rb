require "rails_helper"

RSpec.describe ItemsForSaleResource, type: :resource do
  describe "serialization" do
    let!(:items_for_sale) { create(:items_for_sale) }

    it "works" do
      render
      data = jsonapi_data[0]
      expect(data.id).to eq(items_for_sale.id)
      expect(data.jsonapi_type).to eq("items_for_sales")
    end
  end

  describe "filtering" do
    let!(:items_for_sale1) { create(:items_for_sale) }
    let!(:items_for_sale2) { create(:items_for_sale) }

    context "by id" do
      before do
        params[:filter] = { id: { eq: items_for_sale2.id } }
      end

      it "works" do
        render
        expect(d.map(&:id)).to eq([items_for_sale2.id])
      end
    end
  end

  describe "sorting" do
    describe "by id" do
      let!(:items_for_sale1) { create(:items_for_sale) }
      let!(:items_for_sale2) { create(:items_for_sale) }

      context "when ascending" do
        before do
          params[:sort] = "id"
        end

        it "works" do
          render
          expect(d.map(&:id)).to eq([
                                      items_for_sale1.id,
                                      items_for_sale2.id,
                                    ])
        end
      end

      context "when descending" do
        before do
          params[:sort] = "-id"
        end

        it "works" do
          render
          expect(d.map(&:id)).to eq([
                                      items_for_sale2.id,
                                      items_for_sale1.id,
                                    ])
        end
      end
    end
  end

  describe "sideloading" do
    # ... your tests ...
  end
end
