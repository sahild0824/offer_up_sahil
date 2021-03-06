require "rails_helper"

RSpec.describe ItemsForSale, type: :model do
  describe "Direct Associations" do
    it { should belong_to(:product) }
  end

  describe "InDirect Associations" do
    it { should have_one(:seller) }
  end

  describe "Validations" do
  end
end
