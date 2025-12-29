"""
Animated sprite system for handling sprite sheet animations
"""
import pygame


class AnimatedSprite:
    """Handles sprite sheet animations."""
    
    def __init__(self, sprite_sheet_path, frame_width, frame_height, num_frames, fps, layout='vertical'):
        """
        Initialize animated sprite.
        
        Args:
            sprite_sheet_path: Path to the sprite sheet image
            frame_width: Width of each frame in pixels
            frame_height: Height of each frame in pixels
            num_frames: Total number of frames in the animation
            fps: Frames per second for the animation
            layout: 'horizontal' or 'vertical' arrangement of frames
        """
        # Load the sprite sheet
        try:
            self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Could not load sprite sheet at {sprite_sheet_path}: {e}")
            # Create a fallback surface
            self.sprite_sheet = pygame.Surface((frame_width, frame_height * num_frames))
            self.sprite_sheet.fill((240, 240, 240))
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.fps = fps
        self.layout = layout
        
        # Animation state
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 1.0 / fps  # Time per frame in seconds
        
        # Extract individual frames from sprite sheet
        self.frames = self.load_frames()
    
    def load_frames(self):
        """Extract individual frames from the sprite sheet."""
        frames = []
        
        for i in range(self.num_frames):
            # Create a surface for this frame
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            
            # Calculate source position based on layout
            if self.layout == 'vertical':
                source_rect = pygame.Rect(0, i * self.frame_height, self.frame_width, self.frame_height)
            else:  # horizontal
                source_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            
            # Blit (copy) the frame from sprite sheet
            frame.blit(self.sprite_sheet, (0, 0), source_rect)
            frames.append(frame)
        
        return frames
    
    def update(self, dt):
        """Update animation frame based on time."""
        self.animation_timer += dt
        
        # Move to next frame when enough time has passed
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
    
    def get_current_frame(self):
        """Get the current frame surface."""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset animation to first frame."""
        self.current_frame = 0
        self.animation_timer = 0