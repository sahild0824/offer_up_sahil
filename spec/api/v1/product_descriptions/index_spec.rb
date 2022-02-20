require "rails_helper"

RSpec.describe "product_descriptions#index", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/product_descriptions", params: params
  end

  describe "basic fetch" do
    let!(:product_description1) { create(:product_description) }
    let!(:product_description2) { create(:product_description) }

    it "works" do
      expect(ProductDescriptionResource).to receive(:all).and_call_original
      make_request
      expect(response.status).to eq(200), response.body
      expect(d.map(&:jsonapi_type).uniq).to match_array(["product_descriptions"])
      expect(d.map(&:id)).to match_array([product_description1.id,
                                          product_description2.id])
    end
  end
end
