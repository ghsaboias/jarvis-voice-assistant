import logging
import urllib.parse
import time
from typing import Optional
from src.handlers.apple_script_handler import AppleScriptHandler


class BraveController:
    def __init__(self):
        self.apple_script = AppleScriptHandler()
        self.app_name = "Brave Browser"
        self.common_sites = {
            "youtube": "youtube.com",
            "github": "github.com",
            "netflix": "netflix.com",
            "x": "x.com",
            "twitter": "x.com",
            "facebook": "facebook.com",
            "instagram": "instagram.com",
            "google": "google.com",
            "gmail": "gmail.com",
            "amazon": "amazon.com",
        }

    def activate(self) -> bool:
        """Opens or activates Brave Browser"""
        success, _, _ = self.apple_script.tell_app(self.app_name, "activate")
        return success

    def navigate_to(self, destination: str) -> bool:
        try:
            url = self._format_url(destination)
            # First open a new tab
            if not self.new_tab():
                logging.error("Failed to open new tab for navigation")
                return False

            # Then navigate
            script = f"""
            tell application "Brave Browser"
                activate
                open location "{url}"
            end tell
            """
            success, _, _ = self.apple_script.run_script(script)
            return success
        except Exception as e:
            logging.error(f"Navigation failed: {e}")
            return False

    def _format_url(self, destination: str) -> str:
        # Remove common words
        for word in ["to", "the", "website", "site"]:
            destination = destination.replace(word, "").strip()

        site = destination.lower().strip()

        # Check common sites
        if site in self.common_sites:
            return f"https://{self.common_sites[site]}"

        # Handle direct URLs
        if "." in site:
            return f"https://{site}"

        # Handle search fallback
        return f"https://google.com/search?q={site}"

    def search(self, query: str) -> bool:
        # First open a new tab
        if not self.new_tab():
            logging.error("Failed to open new tab for search")
            return False

        script = (
            """
        tell application "Brave Browser"
            activate
            tell application "System Events"
                keystroke "l" using command down
                delay 0.1
                keystroke "%s"
                delay 0.1
                keystroke return
            end tell
        end tell
        """
            % query
        )
        success, _, _ = self.apple_script.run_script(script)
        return success

    def new_tab(self) -> bool:
        script = """
        tell application "Brave Browser"
            activate
            tell application "System Events"
                keystroke "t" using command down
            end tell
        end tell
        """
        success, _, _ = self.apple_script.run_script(script)
        return success

    def close_tab(self) -> bool:
        script = """
        tell application "Brave Browser"
            activate
            tell application "System Events"
                keystroke "w" using command down
            end tell
        end tell
        """
        success, _, _ = self.apple_script.run_script(script)
        return success

    def youtube_search(self, query: str) -> bool:
        """Search YouTube and wait for results"""
        try:
            encoded_query = urllib.parse.quote(query)
            # Remove the https:// since navigate_to will add it
            url = f"youtube.com/results?search_query={encoded_query}"
            success = self.navigate_to(url)
            if success:
                time.sleep(2)  # Wait for results to load
            return success
        except Exception as e:
            logging.error(f"YouTube search failed: {e}")
            return False

    def select_youtube_result(self, position: int = 1) -> bool:
        """Select video from search results using multiple fallback strategies"""
        try:
            js_script = (
                """
            function selectYouTubeVideo(position) {
                // Helper to check if we're on search results page
                function isSearchPage() {
                    return window.location.pathname.includes('/results');
                }

                // Helper to validate video elements
                function isValidVideo(element) {
                    return element && element.href && element.href.includes('/watch?v=');
                }

                // Log for debugging
                console.log('Attempting to select video position:', position);
                
                if (!isSearchPage()) {
                    console.log('Not on YouTube search page');
                    return false;
                }

                // Strategy 1: Direct video renderer selection
                const videos = document.querySelectorAll('ytd-video-renderer');
                console.log('Found video renderers:', videos.length);
                
                if (!videos.length) {
                    console.log('No video renderers found');
                    return false;
                }

                const targetVideo = videos[position - 1];
                if (!targetVideo) {
                    console.log('Target video position not found');
                    return false;
                }

                // Strategy 2: Try multiple selector types
                const selectors = [
                    'a#video-title',
                    'a#thumbnail',
                    'a[href^="/watch"]'
                ];

                for (const selector of selectors) {
                    const link = targetVideo.querySelector(selector);
                    if (isValidVideo(link)) {
                        console.log('Found valid video link:', link.href);
                        window.location.href = link.href;
                        return true;
                    }
                }

                // Strategy 3: Fallback to any valid video link
                const anyLink = targetVideo.querySelector('a[href*="/watch?v="]');
                if (isValidVideo(anyLink)) {
                    console.log('Using fallback video link:', anyLink.href);
                    window.location.href = anyLink.href;
                    return true;
                }

                console.log('No valid video link found');
                return false;
            }

            // Execute with error handling
            try {
                return selectYouTubeVideo(%d);
            } catch (e) {
                console.error('Error selecting video:', e);
                return false;
            }
            """
                % position
            )

            script = f"""
            tell application "Brave Browser"
                execute javascript "{js_script}"
            end tell
            """

            success, _, stderr = self.apple_script.run_script(script)

            if not success:
                logging.error(f"YouTube video selection failed with stderr: {stderr}")
                return False

            # Wait for video to load, adjust timing based on network
            time.sleep(2)
            return True

        except Exception as e:
            logging.error(f"YouTube video selection failed with exception: {e}")
            return False
