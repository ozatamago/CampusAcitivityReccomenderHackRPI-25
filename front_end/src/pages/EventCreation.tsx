import { useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "../config";
import type { Event } from "../types/backend";

interface EventCreationProps {
  domain: string;
  club_id: 67;
}

export default function EventCreation({ domain, club_id }: EventCreationProps) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    start_time: "",
    end_time: "",
    location: "",
    is_online: false,
    join_link: "",
    capacity: "",
    club_id: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, type, value } = e.target as HTMLInputElement;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const eventPayload: any = {
        title: formData.title,
        description: formData.description || undefined,
        start_time: formData.start_time,
        end_time: formData.end_time,
        location: formData.location || undefined,
        is_online: formData.is_online,
        join_link: formData.join_link || undefined,
        capacity: formData.capacity ? parseInt(formData.capacity) : undefined,
        visibility_mode: "domain",
        visible_email_domains: [domain],
        club_id: formData.club_id ? parseInt(formData.club_id) : undefined,
      };

      const response = await axios.post(
        `${BACKEND_URL}/api/clubs/${club_id}/events`,
        eventPayload
      );
      setMessage("Event created successfully!");
      // Reset form
      setFormData({
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        location: "",
        is_online: false,
        join_link: "",
        capacity: "",
        club_id: "",
      });
    } catch (error) {
      console.error("Failed to create event:", error);
      if (axios.isAxiosError(error)) {
        setMessage(`Error: ${error.response?.data?.error || error.message}`);
      } else {
        setMessage("Failed to create event");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f7f0e6] to-[#fff1f8] p-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Create Event</h1>
        <p className="text-sm text-gray-600 mb-6">
          Creating event visible to domain: <strong>{domain}</strong>
        </p>

        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-lg shadow-lg p-6 space-y-4"
        >
          {/* Title */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Event Title *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="e.g., Weekly Chess Tournament"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="Event details..."
              rows={4}
            />
          </div>

          {/* Start Time */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Start Time *
            </label>
            <input
              type="datetime-local"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          {/* End Time */}
          <div>
            <label className="block text-sm font-medium mb-2">End Time *</label>
            <input
              type="datetime-local"
              name="end_time"
              value={formData.end_time}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium mb-2">Location</label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="e.g., Union Hall Room 204"
            />
          </div>

          {/* Is Online */}
          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                name="is_online"
                checked={formData.is_online}
                onChange={handleChange}
                className="w-4 h-4"
              />
              <span className="text-sm font-medium">Online Event</span>
            </label>
          </div>

          {/* Join Link */}
          {formData.is_online && (
            <div>
              <label className="block text-sm font-medium mb-2">
                Join Link
              </label>
              <input
                type="url"
                name="join_link"
                value={formData.join_link}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded px-3 py-2"
                placeholder="https://meet.google.com/..."
              />
            </div>
          )}

          {/* Capacity */}
          <div>
            <label className="block text-sm font-medium mb-2">Capacity</label>
            <input
              type="number"
              name="capacity"
              value={formData.capacity}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="e.g., 50"
              min="1"
            />
          </div>

          {/* Club ID */}
          <div>
            <label className="block text-sm font-medium mb-2">Club ID</label>
            <input
              type="number"
              name="club_id"
              value={formData.club_id}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="e.g., 1"
              min="1"
            />
          </div>

          {/* Message */}
          {message && (
            <div
              className={`p-3 rounded ${
                message.startsWith("Error")
                  ? "bg-red-100 text-red-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              {message}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded font-medium hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Creating..." : "Create Event"}
          </button>
        </form>
      </div>
    </div>
  );
}
