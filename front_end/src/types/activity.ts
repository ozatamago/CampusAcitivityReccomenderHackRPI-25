// Define the structure for an activity or club
export interface Club {
  id: string;
  title: string;
  type: 'club' | 'event'; // Distinguish between club and event
  description: string;
  tags: string[];
  imageUrl: string;
}