require "rails_helper"

RSpec.describe ItemsForSaleResource, type: :resource do
  describe "creating" do
    let(:payload) do
      {
        data: {
          type: "items_for_sales",
          attributes: {},
        },
      }
    end

    let(:instance) do
      ItemsForSaleResource.build(payload)
    end

    it "works" do
      expect do
        expect(instance.save).to eq(true),
                                 instance.errors.full_messages.to_sentence
      end.to change { ItemsForSale.count }.by(1)
    end
  end

  describe "updating" do
    let!(:items_for_sale) { create(:items_for_sale) }

    let(:payload) do
      {
        data: {
          id: items_for_sale.id.to_s,
          type: "items_for_sales",
          attributes: {}, # Todo!
        },
      }
    end

    let(:instance) do
      ItemsForSaleResource.find(payload)
    end

    xit "works (add some attributes and enable this spec)" do
      expect do
        expect(instance.update_attributes).to eq(true)
      end.to change { items_for_sale.reload.updated_at }
      # .and change { items_for_sale.foo }.to('bar') <- example
    end
  end

  describe "destroying" do
    let!(:items_for_sale) { create(:items_for_sale) }

    let(:instance) do
      ItemsForSaleResource.find(id: items_for_sale.id)
    end

    it "works" do
      expect do
        expect(instance.destroy).to eq(true)
      end.to change { ItemsForSale.count }.by(-1)
    end
  end
end
