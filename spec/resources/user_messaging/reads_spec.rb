require "rails_helper"

RSpec.describe UserMessagingResource, type: :resource do
  describe "serialization" do
    let!(:user_messaging) { create(:user_messaging) }

    it "works" do
      render
      data = jsonapi_data[0]
      expect(data.id).to eq(user_messaging.id)
      expect(data.jsonapi_type).to eq("user_messagings")
    end
  end

  describe "filtering" do
    let!(:user_messaging1) { create(:user_messaging) }
    let!(:user_messaging2) { create(:user_messaging) }

    context "by id" do
      before do
        params[:filter] = { id: { eq: user_messaging2.id } }
      end

      it "works" do
        render
        expect(d.map(&:id)).to eq([user_messaging2.id])
      end
    end
  end

  describe "sorting" do
    describe "by id" do
      let!(:user_messaging1) { create(:user_messaging) }
      let!(:user_messaging2) { create(:user_messaging) }

      context "when ascending" do
        before do
          params[:sort] = "id"
        end

        it "works" do
          render
          expect(d.map(&:id)).to eq([
                                      user_messaging1.id,
                                      user_messaging2.id,
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
                                      user_messaging2.id,
                                      user_messaging1.id,
                                    ])
        end
      end
    end
  end

  describe "sideloading" do
    # ... your tests ...
  end
end
